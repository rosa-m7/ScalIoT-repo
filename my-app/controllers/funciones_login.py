from datetime import datetime
from conexion.conexionBD import connectionBD
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, flash

# --- Funciones de Login y Registro ---

def dataLoginSesion():
    """
    Retorna los datos de sesión del usuario conectado.
    """
    dataLogin = {
        "id": session.get("id"),
        "name": session.get("name"),
        "cedula": session.get("cedula"),
        "rol": session.get("rol"),
        "conectado": session.get("conectado")
    }
    return dataLogin

def info_perfil_session(id_usuario):
    """
    Obtiene la información completa del perfil de un usuario por su ID (adaptado a sistema_motricidad).
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        u.id_usuario, u.cedula, u.nombre, u.apellido, 
                        u.email, u.telefono, u.fecha_creacion, u.activo, 
                        u.id_rol, r.nombre_rol, u.password,
                        u.especialidad, u.anos_experiencia, u.certificaciones
                    FROM usuario u
                    INNER JOIN rol r ON u.id_rol = r.id_rol
                    WHERE u.id_usuario = %s
                """
                cursor.execute(querySQL, (id_usuario,))
                info_perfil = cursor.fetchone()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session: {e}")
        return None

def recibeInsertRegisterUser(cedula, nombre, apellido, email, telefono, id_rol, pass_user, especialidad=None, anos_experiencia=None, certificaciones=None):
    """
    Inserta un nuevo usuario en la base de datos 'usuario' de sistema_motricidad.
    Los campos de evaluador solo se usan si el rol es evaluador (id_rol == 2).
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                sql = """
                    INSERT INTO usuario (
                        cedula, nombre, apellido, email, telefono, password, id_rol, especialidad, anos_experiencia, certificaciones
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    cedula, nombre, apellido, email, telefono,
                    generate_password_hash(pass_user), id_rol,
                    especialidad if id_rol == 2 else None,
                    anos_experiencia if id_rol == 2 else None,
                    certificaciones if id_rol == 2 else None
                )
                mycursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return mycursor.lastrowid
    except Exception as e:
        flash(f'Se produjo un error al registrar el usuario: {str(e)}', 'error')
        return False

# La función insertarDatosEvaluador ya no es necesaria porque los datos de evaluador están en la tabla usuario.
# Puedes eliminarla o dejarla como referencia histórica, pero no debe usarse más.

from werkzeug.security import generate_password_hash, check_password_hash
# Asegúrate de que connectionBD esté importado o definido en algún lugar accesible

def procesar_update_perfil(form_data, id_usuario):
    """
    Actualiza los datos del perfil de un usuario en la nueva base 'usuario'.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                cedula = form_data['cedula']
                nombre = form_data['name']
                apellido = form_data['surname']
                email = form_data['email']
                telefono = form_data['telefono']
                id_rol = int(form_data['selectRol'])

                # --- Nombres correctos de los campos del formulario HTML ---
                pass_actual_from_form = form_data.get('pass_actual')
                new_pass_user_from_form = form_data.get('new_pass_user')
                repetir_pass_user_from_form = form_data.get('repetir_pass_user')

                # Manejo de campos de evaluador. Usamos .get() con None como valor por defecto.
                especialidad = form_data.get('especialidad', None)
                anos_experiencia_str = form_data.get('anos_experiencia', None)
                anos_experiencia = int(anos_experiencia_str) if anos_experiencia_str and anos_experiencia_str.isdigit() else None
                certificaciones = form_data.get('certificaciones', None)

                # 1. Obtener la contraseña actual del usuario de la base de datos
                mycursor.execute("SELECT password FROM usuario WHERE id_usuario = %s", (id_usuario,))
                user_account = mycursor.fetchone()
                
                if not user_account:
                    print(f"DEBUG: Usuario con ID {id_usuario} no encontrado en la BD.")
                    return -1 # Usuario no existe, error crítico

                hashed_password_in_db = user_account['password']
                print(f"[DEBUG][procesar_update_perfil] Valor recibido en pass_actual_from_form: '{pass_actual_from_form}'")
                print(f"[DEBUG][procesar_update_perfil] Hash recuperado de la BD: '{hashed_password_in_db}'")

                # 2. Lógica para el cambio de contraseña
                new_password_to_update = None 
                
                # --- CAMBIO CLAVE AQUÍ: Solo entra en la lógica de contraseña si realmente hay una NUEVA contraseña ---
                if new_pass_user_from_form and new_pass_user_from_form.strip(): # `strip()` para evitar espacios en blanco
                    print("DEBUG: Se detectó intento de cambio de contraseña (new_pass_user_from_form tiene contenido).")
                    
                    if not pass_actual_from_form or not pass_actual_from_form.strip():
                        print("DEBUG: pass_actual_from_form está vacío o solo tiene espacios.")
                        return 3 # La clave actual es obligatoria si se quiere cambiar la nueva

                    # Verificar la contraseña actual ingresada por el usuario
                    resultado_check = check_password_hash(hashed_password_in_db, pass_actual_from_form)
                    print(f"[DEBUG][procesar_update_perfil] Resultado de check_password_hash: {resultado_check}")
                    if not resultado_check:
                        print("DEBUG: Contraseña actual incorrecta.")
                        return 0 # Contraseña actual incorrecta

                    # Verificar que la nueva contraseña y la confirmación coincidan
                    if new_pass_user_from_form != repetir_pass_user_from_form:
                        print("DEBUG: Nueva contraseña y confirmación no coinciden.")
                        return 2 # Ambas claves deben ser iguales

                    # Si todas las verificaciones pasan, hashear la nueva contraseña
                    new_password_to_update = generate_password_hash(new_pass_user_from_form)
                    print("DEBUG: Nueva contraseña hasheada y lista para actualizar.")
                else:
                    print("DEBUG: No se intentó cambiar la contraseña (new_pass_user_from_form vacío o None).")

                # 3. Leer el valor de 'activo' del formulario
                activo = 1 if form_data.get('activo') == '1' else 0

                # 4. Construir dinámicamente la consulta SQL y los valores
                sql_set_parts = [
                    "cedula = %s", 
                    "nombre = %s", 
                    "apellido = %s", 
                    "email = %s", 
                    "telefono = %s", 
                    "id_rol = %s",
                    "especialidad = %s",
                    "anos_experiencia = %s",
                    "certificaciones = %s",
                    "activo = %s"  # <-- AGREGADO
                ]
                 
                valores_a_enviar = [
                    cedula, nombre, apellido, email, telefono, id_rol,
                    especialidad if id_rol == 2 else None,
                    anos_experiencia if id_rol == 2 else None,
                    certificaciones if id_rol == 2 else None,
                    activo  # <-- AGREGADO
                ]

                # Añadir la contraseña si se va a actualizar
                if new_password_to_update is not None:
                    sql_set_parts.append("password = %s")
                    valores_a_enviar.append(new_password_to_update)

                # Construir la consulta SQL final para usuario
                sql_update = f"UPDATE usuario SET {', '.join(sql_set_parts)} WHERE id_usuario = %s"
                valores_a_enviar.append(id_usuario)

                print("--- DEPURACIÓN SQL USUARIO ---")
                print(f"SQL Final: {sql_update}")
                print(f"Valores a enviar: {valores_a_enviar}")
                print(f"Cantidad de %s en SQL: {sql_update.count('%s')}")
                print(f"Cantidad de valores: {len(valores_a_enviar)}")
                print("-----------------------")

                mycursor.execute(sql_update, valores_a_enviar)
                conexion_MySQLdb.commit()

                return 1 # Éxito
    except Exception as e:
        print(f'ERROR: Se produjo un error al actualizar el perfil: {str(e)}')
        return -2
        return -1

def insertar_acceso_registro(id_usuario, tipo_acceso, cedula_ingresada, ip_address, user_agent):
    """
    Inserta un registro de acceso en la tabla 'accesos'.
    :param id_usuario: ID del usuario (puede ser None para inicios de sesión fallidos sin usuario existente).
    :param tipo_acceso: 'login', 'logout' o 'failed_login'.
    :param cedula_ingresada: La cédula que se intentó usar para el acceso.
    :param ip_address: Dirección IP del cliente.
    :param user_agent: User-Agent del cliente.
    :return: True si la inserción fue exitosa, False en caso contrario.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    INSERT INTO acceso (id_usuario, fecha_acceso, ip_address, user_agent, tipo_acceso)
                    VALUES (%s, %s, %s, %s, %s)
                """
                # Obtener la hora de Ecuador para guardar en la base de datos (corrige desfase horario en Cloud Run)
                from app import get_ecuador_time
                fecha_acceso = get_ecuador_time()
                user_id_to_insert = id_usuario if id_usuario is not None else None 
                cursor.execute(sql, (user_id_to_insert, fecha_acceso, ip_address, user_agent, tipo_acceso))
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error al insertar registro de acceso: {e}")
        return False

