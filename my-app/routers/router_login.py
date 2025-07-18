from app import app
from flask import render_template, request, flash, redirect, url_for, session
from flask import jsonify
from controllers.funciones_home import obtenerroles, accesosReporte, generarReporteExcel
# Importaciones necesarias

import os

# Importaciones de tus controladores (mantener como estaban)
from controllers.funciones_home import obtenerroles, accesosReporte, generarReporteExcel
from controllers.funciones_login import (
    dataLoginSesion, info_perfil_session, recibeInsertRegisterUser,
    procesar_update_perfil, insertar_acceso_registro
)
from conexion.conexionBD import connectionBD
from werkzeug.security import check_password_hash
import firebase_admin
from firebase_admin import credentials, db
import os # Para manejar la ruta del archivo de credenciales
# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
# MODIFICACIÓN: Importación explícita de las funciones necesarias
from controllers.funciones_login import (
    dataLoginSesion, info_perfil_session, recibeInsertRegisterUser,
    procesar_update_perfil, insertar_acceso_registro
)
from controllers.funciones_home import * # Mantener esta importación como estaba

PATH_URL_LOGIN = "/public/login"

# --- Configuración de Firebase ---
# Ir hacia la carpeta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'key_firebase.json')

# Verifica si Firebase ya ha sido inicializado para evitar errores en recargas de desarrollo
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://db-maldonado-default-rtdb.firebaseio.com/'
        })
        print("Firebase Admin SDK inicializado correctamente.")
    except Exception as e:
        print(f"Error al inicializar Firebase Admin SDK: {e}")
        exit(1) # Salir si Firebase no se puede inicializar

# Obtener referencias a la base de datos para el modo y el estado de la evaluación
# El modo se guarda como un string plano en la raíz 'modo'
ref_modo = db.reference('modo')
# El estado de activación se guarda en 'evaluacionActual/activa'
ref_evaluacion_actual = db.reference('evaluacionActual')
# Referencia al nodo 'ninos'
ref_ninos = db.reference('ninos')


# --- Rutas de la Interfaz Web ---

# La ruta '/' se puede definir si es necesario, pero no incluirá la lógica de agregar un niño aquí.
# @app.route('/')
# def index():
#     return "Bienvenido a la aplicación Flask"


@app.route('/control_sesion')
def control_sesion():
    """
    Ruta para la interfaz de control de modo y estado de sesión.
    Carga la plantilla HTML que contendrá la lógica de polling y control.
    """
    print('[DEBUG][control_sesion] session al entrar a control_sesion:', dict(session))
    id_usuario = session.get("id")
    rol = session.get("rol")
    dataLogin = {
        "id": id_usuario,
        "rol": rol
    }
    return render_template('public/sesion/control_sesion.html', dataLogin=dataLogin)


# --- Rutas de la API para control de Modo de Firebase ---

@app.route('/api/sesiones', methods=['GET'])
def listar_sesiones():
    """
    Endpoint para obtener la lista de sesiones desde la base de datos MySQL.
    Permite filtros opcionales por id_nino, id_usuario, estado, tipo_evaluacion, fecha_inicio y fecha_fin.
    """
    try:
        id_nino = request.args.get('id_nino')
        id_usuario = request.args.get('id_usuario')
        estado = request.args.get('estado')
        tipo_evaluacion = request.args.get('tipo_evaluacion')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')

        query = "SELECT id_sesion, id_nino, id_usuario, session_id_firebase, fecha_sesion, tipo_evaluacion, estado, observaciones_inicio, observaciones_final, sincronizado_firebase, fecha_creacion FROM sesion WHERE 1=1"
        params = []

        if id_nino:
            query += " AND id_nino = %s"
            params.append(id_nino)
        if id_usuario:
            query += " AND id_usuario = %s"
            params.append(id_usuario)
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        if tipo_evaluacion:
            query += " AND tipo_evaluacion = %s"
            params.append(tipo_evaluacion)
        if fecha_inicio:
            query += " AND fecha_sesion >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND fecha_sesion <= %s"
            params.append(fecha_fin)

        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                sesiones = cursor.fetchall()
        return jsonify({"sesiones": sesiones}), 200
    except Exception as e:
        print(f"Error al listar sesiones: {e}")
        return jsonify({"error": "Error al obtener las sesiones", "details": str(e)}), 500


@app.route('/api/modo/estado', methods=['GET'])
def get_modo_estado():
    """
    Endpoint de API para obtener el estado actual del modo desde Firebase.
    Devuelve un JSON con el modo actual.
    """
    try:
        modo_actual = ref_modo.get()
        # Si no hay un modo establecido en Firebase, se devuelve "ninguno" por defecto.
        # Esto es útil para la interfaz de usuario.
        if modo_actual is None:
            modo_actual = "ninguno"
        return jsonify({'modo': modo_actual}), 200
    except Exception as e:
        print(f"Error al obtener el estado del modo: {e}")
        return jsonify({'error': 'Error al obtener el estado del modo'}), 500

@app.route('/api/modo/actualizar', methods=['POST'])
def actualizar_modo():
    """
    Endpoint de API para actualizar el modo en Firebase.
    Valida el nuevo modo y solo lo actualiza si ha cambiado.
    """
    data = request.get_json()
    nuevo_modo = data.get('modo')

    modos_validos = ["evaluacion", "juego", "descanso"]

    # Validación del modo recibido
    if not nuevo_modo or nuevo_modo not in modos_validos:
        return jsonify({'error': 'Modo inválido. Debe ser "evaluacion", "juego" o "descanso".'}), 400

    try:
        # Obtener el modo actual de Firebase para comparar
        modo_actual_firebase = ref_modo.get()

        # Solo actualizar si el nuevo modo es diferente al actual
        if modo_actual_firebase == nuevo_modo:
            return jsonify({'message': f'El modo ya es "{nuevo_modo}". No se realizó ninguna actualización.', 'modo': nuevo_modo}), 200

        # Si es diferente, actualizar en Firebase
        ref_modo.set(nuevo_modo)
        return jsonify({'message': f'Modo actualizado a "{nuevo_modo}" correctamente.', 'modo': nuevo_modo}), 200
    except Exception as e:
        print(f"Error al actualizar el modo: {e}")
        return jsonify({'error': 'Error al actualizar el modo'}), 500

# --- Rutas de la API para control de Estado de Sesión (Activa/Inactiva) ---

@app.route('/api/sesion/estado', methods=['GET'])
def get_sesion_estado():
    """
    Endpoint de API para obtener el estado actual de la sesión (activa/inactiva) desde Firebase.
    Devuelve un JSON con el estado 'activa'.
    """
    try:
        activa_ref = ref_evaluacion_actual.child('activa')
        estado = activa_ref.get()
        # Asegurarse de que el estado sea 0 o 1, o un valor por defecto si no existe
        estado = 1 if estado == 1 else 0
        return jsonify({'activa': estado}), 200
    except Exception as e:
        print(f"Error al obtener el estado de la sesión: {e}")
        return jsonify({'error': 'Error al obtener el estado de la sesión'}), 500

@app.route('/api/sesion/iniciar', methods=['POST'])
def iniciar_sesion():
    """
    Inicia una nueva sesión para un niño, usando el usuario logueado, y registra en la tabla 'sesion'.
    Espera: id_nino, tipo_evaluacion (opcional), observaciones_inicio (opcional)
    """
    from flask import session as flask_session
    from datetime import datetime
    data = request.get_json()
    id_nino = data.get('id_nino')  # Ahora toma el id del niño seleccionado en el frontend
    tipo_evaluacion = data.get('tipo_evaluacion', 'diagnóstica')
    observaciones_inicio = data.get('observaciones_inicio', None)
    id_usuario = flask_session.get('id')  # Evaluador siempre es el usuario logueado
    sincronizado_firebase = 0
    session_id_firebase = None
    estado = 'en_curso'

    print(f"[DEBUG] id_nino recibido: {id_nino}")
    print(f"[DEBUG] id_usuario (logueado) recibido: {id_usuario}")
    print(f"[DEBUG] tipo_evaluacion: {tipo_evaluacion}")

    if not id_nino or not id_usuario:
        print("[DEBUG] Faltan datos para iniciar la sesión")
        return jsonify({'error': 'Faltan datos para iniciar la sesión.'}), 400

    try:
        # Buscar código_nino y nombre para Firebase
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT codigo_nino, CONCAT(nombre, ' ', apellido) as nombre_completo FROM nino WHERE id_nino = %s", (id_nino,))
                nino = cursor.fetchone()
        if not nino:
            print("[DEBUG] No se encontró el niño en la base de datos por id_nino")
            return jsonify({'error': 'No se encontró el niño/a en la base de datos.'}), 404
        codigo_nino = nino['codigo_nino']
        nombre_nino = nino['nombre_completo']

        # Firebase sync
        nodo_nino = f"nino-id-{id_nino}"
        ref_nino_firebase = ref_ninos.child(nodo_nino)
        fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        data_nino = ref_nino_firebase.get()
        try:
            if data_nino is not None:
                ref_nino_firebase.update({'nombre': nombre_nino})
                ref_nino_firebase.child('sesiones').update({fecha_actual: True})
            else:
                ref_nino_firebase.set({
                    'nombre': nombre_nino,
                    'sesiones': {fecha_actual: True}
                })
            sincronizado_firebase = 1
            session_id_firebase = fecha_actual
        except Exception as firebase_err:
            print(f"[DEBUG] Error sincronizando con Firebase: {firebase_err}")
            sincronizado_firebase = 0

        # Insertar en la tabla 'sesion'
        print(f"[DEBUG] Insertando en sesion: id_nino={id_nino}, id_usuario={id_usuario}")
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sesion (
                        id_nino, id_usuario, session_id_firebase, fecha_sesion, tipo_evaluacion, estado, observaciones_inicio, sincronizado_firebase
                    ) VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s)
                """, (
                    id_nino, id_usuario, session_id_firebase, tipo_evaluacion, estado, observaciones_inicio, sincronizado_firebase
                ))
                conexion.commit()
        print("[DEBUG] Inserción en sesion completada")

        # Activar la sesión en Firebase
        activa_ref = ref_evaluacion_actual.child('activa')
        current_state = activa_ref.get()
        if current_state == 1:
            return jsonify({'message': 'La sesión ya está activa.'}), 200
        activa_ref.set(1)
        return jsonify({'message': 'Sesión iniciada correctamente.', 'activa': 1}), 200
    except Exception as e:
        print(f"Error al iniciar la sesión: {e}")
        return jsonify({'error': 'Error al iniciar la sesión'}), 500


@app.route('/api/sesion/finalizar', methods=['POST'])
def finalizar_sesion():
    """
    Finaliza la sesión 'en_curso' más reciente para un niño, actualizando estado y observaciones.
    Espera: id_nino, observaciones_final (opcional)
    """
    from datetime import datetime
    data = request.get_json()
    id_nino = data.get('id_nino')
    observaciones_final = data.get('observaciones_final', None)
    sincronizado_firebase = 0

    if not id_nino:
        return jsonify({'error': 'El id_nino es requerido para finalizar la sesión.'}), 400

    try:
        # Buscar el nombre del niño en la base de datos
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT codigo_nino, CONCAT(nombre, ' ', apellido) as nombre_completo FROM nino WHERE id_nino = %s", (id_nino,))
                nino = cursor.fetchone()
        if not nino:
            return jsonify({'error': 'No se encontró el niño/a en la base de datos.'}), 404
        codigo_nino = nino['codigo_nino']
        nombre_nino = nino['nombre_completo']

        # Firebase sync
        activa_ref = ref_evaluacion_actual.child('activa')
        current_state = activa_ref.get()
        try:
            if current_state == 0:
                return jsonify({'message': 'La sesión ya está inactiva.'}), 200
            activa_ref.set(0)
            sincronizado_firebase = 1
        except Exception as firebase_err:
            print(f"[DEBUG] Error sincronizando con Firebase: {firebase_err}")
            sincronizado_firebase = 0

        # Actualizar la sesión más reciente (en_curso) para este niño
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE sesion
                    SET estado = 'completada', observaciones_final = %s, sincronizado_firebase = %s
                    WHERE id_nino = %s AND estado = 'en_curso'
                    ORDER BY fecha_sesion DESC
                    LIMIT 1
                """, (
                    observaciones_final, sincronizado_firebase, id_nino
                ))
                conexion.commit()
        print("[DEBUG] Actualización de estado y observaciones en sesion completada")

        return jsonify({'message': 'Sesión finalizada correctamente.', 'activa': 0}), 200
    except Exception as e:
        print(f"Error al finalizar la sesión: {e}")
        return jsonify({'error': 'Error al finalizar la sesión'}), 500




# --- Mantener tus otras rutas existentes aquí ---
# Por ejemplo:
# @app.route('/')
# def index():
#     return "Bienvenido a la aplicación Flask"

# Puedes añadir aquí tus otras rutas de la aplicación (gestión de niños, etc.)
# @app.route('/public/login')
# def loginCliente():
#     return render_template('public/login.html')

# if __name__ == '__main__':
#     if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
#         print(f"Error: El archivo de credenciales de Firebase no se encontró en '{FIREBASE_CREDENTIALS_PATH}'.")
#         print("Por favor, descarga tu 'serviceAccountKey.json' de Firebase y colócalo en la ruta correcta.")
#     else:
#         app.run(debug=True, port=5000) # Ejecuta la aplicación en modo debug

@app.route('/', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/mi-perfil/<string:id>', methods=['GET'])
def perfil(id):
    if 'conectado' in session:
        info_usuario = info_perfil_session(id)
        # Los datos de evaluador ya están en info_usuario si aplica
        return render_template(
            'public/perfil/perfil.html',
            info_perfil_session=info_usuario,
            dataLogin=dataLoginSesion(),
            roles=lista_rolesBD()
        )
    else:
        return redirect(url_for('inicio'))


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    # Ya no se usa 'areas', solo roles
    return render_template(f'{PATH_URL_LOGIN}/auth_register.html', dataLogin=dataLoginSesion(), roles=lista_rolesBD())


# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


@app.route('/register-user', methods=['POST'])
def cpanelRegisterUserBD():
    try:
        cedula = request.form['cedula']
        nombre = request.form['name']
        apellido = request.form['surname']
        email = request.form['email']
        telefono = request.form['telefono']
        id_rol = int(request.form['selectRol'])
        pass_user = request.form['pass_user']

        # Solo para evaluadores (rol 2)
        especialidad = request.form.get('especialidad', None) if id_rol == 2 else None
        anos_experiencia = request.form.get('anos_experiencia', None) if id_rol == 2 else None
        certificaciones = request.form.get('certificaciones', None) if id_rol == 2 else None
        if anos_experiencia:
            try:
                anos_experiencia = int(anos_experiencia)
            except ValueError:
                anos_experiencia = None

        id_usuario_creado = recibeInsertRegisterUser(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            id_rol=id_rol,
            pass_user=pass_user,
            especialidad=especialidad,
            anos_experiencia=anos_experiencia,
            certificaciones=certificaciones
        )

        if id_usuario_creado:
            flash('Usuario registrado exitosamente!', 'success')
            return redirect(url_for('usuarios'))
        else:
            return redirect(url_for('cpanelRegisterUser'))

    except KeyError as e:
        flash(f'Falta un campo requerido en el formulario: {e}', 'error')
        return redirect(url_for('cpanelRegisterUser'))
    except Exception as e:
        flash(f'Ocurrió un error inesperado al procesar el registro: {e}', 'error')
        print(f"Error en cpanelRegisterUserBD: {e}")
        return redirect(url_for('cpanelRegisterUser'))


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil/<int:id>", methods=['POST'])
def actualizarPerfil(id):
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form,id)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil',id=id))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil',id=id))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil',id=id))
            else: 
                flash('Clave actual incorrecta', 'error') # Este else es un poco genérico, revisar si es necesario
                return redirect(url_for('perfil',id=id))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'cedula' in request.form and 'pass_user' in request.form:

            cedula = str(request.form['cedula'])
            pass_user = str(request.form['pass_user'])
            conexion_MySQLdb = connectionBD()
            print(conexion_MySQLdb)
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM usuario WHERE cedula = %s", [cedula])
            account = cursor.fetchone()

            # Obtener IP y User-Agent
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            if account:
                if check_password_hash(account['password'], pass_user):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    session['id'] = account['id_usuario']
                    session['name'] = account['nombre']
                    session['cedula'] = account['cedula']
                    session['rol'] = account['id_rol']

                    # Registrar acceso exitoso
                    insertar_acceso_registro(account['id_usuario'], 'login', cedula, ip_address, user_agent)

                    print('[DEBUG][loginCliente] session después de login:', dict(session))
                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('inicio'))
                else:
                    # Registrar acceso fallido (contraseña incorrecta)
                    insertar_acceso_registro(account['id_usuario'], 'failed_login', cedula, ip_address, user_agent)

                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                # Registrar acceso fallido (usuario no encontrado)
                # En este caso, id_usuario es None porque el usuario no existe en la BD
                insertar_acceso_registro(None, 'failed_login', cedula, ip_address, user_agent) 

                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Capturar información para el registro de logout antes de limpiar la sesión
            user_id = session.get('id')
            user_cedula = session.get('cedula')
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name', None)
            session.pop('cedula', None)
            session.pop('rol', None)
            
            # Registrar logout
            insertar_acceso_registro(user_id, 'logout', user_cedula, ip_address, user_agent)
            
            flash('tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
#--------------------- metodo de graficas ----------------------

@app.route('/lista-de-graficas')
def lista_de_graficas():
    if 'conectado' in session:
        # Simulación de datos de sesión para dataLogin
        dataLogin = {
            "id": session.get("id"),
            "rol": session.get("rol"),  # Asegúrate de que 'rol' esté en la sesión
        }
        return render_template('public/grafica/lista_graficas.html', dataLogin=dataLogin)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))
    #-----------------------------------------------------------
@app.route('/grafica_roles_datos', methods=['GET'])
def grafica_roles_datos():
    try:
        roles = obtenerroles()  # Llama a la función que obtiene los datos de roles
        nombres = [rol['nombre_rol'] for rol in roles]
        return jsonify({"nombres": nombres})  # Devuelve solo los nombres de los roles
    except Exception as e:
        print(f"Error en grafica_roles_datos: {e}")
        return jsonify({"error": "Error al obtener los datos"}), 500
    
    #--------------------- areas -----------------------------------
@app.route('/grafica_areas_datos', methods=['GET'])
def grafica_areas_datos():
    try:
        areas = obtener_areas()  # Llama a la función que obtiene los datos de las áreas
        nombres = [area['nombre_area'] for area in areas]
        cantidades = [area['numero_personas'] for area in areas]
        return jsonify({"nombres": nombres, "cantidades": cantidades})  # Devuelve los datos en formato JSON
    except Exception as e:
        print(f"Error en grafica_areas_datos: {e}")
        return jsonify({"error": "Error al obtener los datos"}), 500
    #-------------------------------- accesos a datos--------------------
@app.route('/grafica_accesos_datos', methods=['GET'])
def grafica_accesos_datos():
    try:
        # Obtener las fechas de los parámetros de la URL
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debe proporcionar las fechas de inicio y fin"}), 400

        accesos = obtener_accesos_por_fecha(fecha_inicio, fecha_fin)
        claves = [acceso['clave'] for acceso in accesos]
        cantidades = [acceso['cantidad'] for acceso in accesos]

        return jsonify({"claves": claves, "cantidades": cantidades})
    except Exception as e:
        print(f"Error en grafica_accesos_datos: {e}")
        return jsonify({"error": "Error al obtener los datos"}), 500
    #------------------------ acesso de datos por usuario---------------------
@app.route('/obtener_nombres_usuarios', methods=['GET'])
def obtener_nombres_usuarios():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = '''
                    SELECT id_usuario, nombre
                    FROM usuario
                    WHERE id_rol = 2
                    ORDER BY nombre ASC
                '''
                cursor.execute(query)
                evaluadores = cursor.fetchall()
        return jsonify({"evaluadores": evaluadores})
    except Exception as e:
        print(f"Error en obtener_nombres_usuarios: {e}")
        return jsonify({"error": "Error al obtener los evaluadores"}), 500
    
@app.route('/grafica_fechas_usuario_datos', methods=['GET'])


#---------------------------------------------------------------------
def grafica_fechas_usuario_datos():
    try:
        # Obtener el nombre del usuario de los parámetros de la URL
        nombre = request.args.get('nombre')

        if not nombre:
            return jsonify({"error": "Debe proporcionar el nombre del usuario"}), 400

        # Consultar las fechas de acceso del usuario
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT a.fecha_acceso AS fecha
                    FROM accesos a
                    INNER JOIN usuario u ON a.id_usuario = u.id_usuario
                    WHERE u.nombre = %s
                    ORDER BY a.fecha_acceso ASC
                """
                cursor.execute(query, (nombre,))
                accesos = cursor.fetchall()

        # Preparar los datos para la gráfica
        fechas = [acceso['fecha'] for acceso in accesos]

        return jsonify({"fechas": fechas})
    except Exception as e:
        print(f"Error en grafica_fechas_usuario_datos: {e}")
        return jsonify({"error": "Error al obtener los datos"}), 500
    

# --- Rutas para la gestión de Niños ---

@app.route('/ninos')
def gestionar_ninos():
    # Aquí puedes añadir una verificación de sesión si quieres que solo usuarios con rol específico vean esto
    # if 'conectado' not in session or session.get('rol') != 1: # Ejemplo de verificación de rol de administrador
    #     flash('Acceso denegado. No tienes permisos para gestionar niños.', 'error')
    #     return redirect(url_for('loginCliente'))
    
    ninos = lista_ninoBD()
    dataLogin = { # Simulación de dataLogin si la necesitas en la plantilla para el menú, etc.
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/ninos/lista_ninos.html', ninos=ninos, dataLogin=dataLogin)

from controllers.funciones_home import generar_codigo_nino  # Asegúrate de que esta función exista

@app.route('/ninos/agregar', methods=['GET', 'POST'])
def agregar_nino():
    if request.method == 'POST':
        # Generar código automáticamente
        codigo_nino = generar_codigo_nino()

        # Recoger el resto de campos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        id_genero = int(request.form['id_genero'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        observaciones = request.form['observaciones']
        tutor_responsable = request.form['tutor_responsable']
        telefono_contacto = request.form['telefono_contacto']
        email_contacto = request.form['email_contacto']
        activo = True if request.form.get('activo') == 'on' else False

        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha de nacimiento inválido. Use AAAA-MM-DD.', 'error')
            dataLogin = {
                "id": session.get("id"),
                "rol": session.get("rol"),
            }
            nino = {
                "codigo_nino": "", "nombre": nombre, "apellido": apellido,
                "fecha_nacimiento": fecha_nacimiento_str,
                "id_genero": id_genero, "peso": peso, "altura": altura,
                "observaciones": observaciones,
                "tutor_responsable": tutor_responsable, "telefono_contacto": telefono_contacto,
                "email_contacto": email_contacto, "activo": activo
            }
            return render_template('public/ninos/agregar_nino.html', dataLogin=dataLogin, nino=nino)

        fecha_registro = datetime.datetime.now()
        ultima_actualizacion = datetime.datetime.now()

        resultado = guardar_ninoBD(
            codigo_nino, nombre, apellido, fecha_nacimiento, id_genero, peso, altura,
            tutor_responsable, telefono_contacto, email_contacto, observaciones, activo, fecha_registro
        )
        if resultado > 0:
            flash(f'Niño agregado exitosamente con código {codigo_nino}!', 'success')
            return redirect(url_for('gestionar_ninos'))
        else:
            flash('Error al agregar el niño.', 'error')

    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    nino = {
        "codigo_nino": "", "nombre": "", "apellido": "", "fecha_nacimiento": "",
        "id_genero": 1, "peso": 0.0, "altura": 0.0, "observaciones_generales": "",
        "tutor_responsable": "", "telefono_contacto": "", "email_contacto": "",
        "activo": True
    }
    return render_template('public/ninos/agregar_nino.html', dataLogin=dataLogin, nino=nino)


@app.route('/ninos/editar/<int:id>', methods=['GET', 'POST'])
def editar_nino(id):
    nino = obtener_nino_por_idBD(id)
    if not nino:
        flash('Niño no encontrado.', 'error')
        return redirect(url_for('gestionar_ninos'))

    # Preparar nino para mostrar en el template (GET o POST inicial)
    # Convertir fecha a string para el input HTML
    if 'fecha_nacimiento' in nino and isinstance(nino['fecha_nacimiento'], (datetime.datetime, datetime.date)):
        nino['fecha_nacimiento'] = nino['fecha_nacimiento'].strftime('%Y-%m-%d')
    elif 'fecha_nacimiento' not in nino or nino['fecha_nacimiento'] is None:
        nino['fecha_nacimiento'] = ''

    if request.method == 'POST':
        # No se actualiza código_nino (solo para referencia)
        codigo_nino = nino['codigo_nino']

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento_input_str = request.form['fecha_nacimiento']
        id_genero = int(request.form['id_genero'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        observaciones = request.form['observaciones']
        tutor_responsable = request.form['tutor_responsable']
        telefono_contacto = request.form['telefono_contacto']
        email_contacto = request.form['email_contacto']
        activo = 1 if request.form.get('activo') == '1' else 0

        try:
            fecha_nacimiento_obj = datetime.datetime.strptime(fecha_nacimiento_input_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha de nacimiento inválido. Use AAAA-MM-DD.', 'error')
            nino['fecha_nacimiento'] = fecha_nacimiento_input_str
            dataLogin = {
                "id": session.get("id"),
                "rol": session.get("rol"),
            }
            return render_template('public/ninos/editar_nino.html', nino=nino, dataLogin=dataLogin)

        ultima_actualizacion = datetime.datetime.now()

        resultado = actualizar_ninoBD(
            id, nombre, apellido, fecha_nacimiento_obj, id_genero, peso, altura,
            tutor_responsable, telefono_contacto, email_contacto, observaciones, activo
        )
        if resultado > 0:
            flash('Niño actualizado exitosamente!', 'success')
            return redirect(url_for('gestionar_ninos'))
        else:
            flash('Error al actualizar el niño.', 'error')
            if fecha_nacimiento_obj:
                nino['fecha_nacimiento'] = fecha_nacimiento_obj.strftime('%Y-%m-%d')

    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/ninos/editar_nino.html', nino=nino, dataLogin=dataLogin)

@app.route('/ninos/eliminar/<int:id>')
def eliminar_nino(id):
    # Similar, puedes añadir verificación de sesión aquí
    resultado = eliminar_ninoBD(id)
    if resultado > 0:
        flash('Niño eliminado exitosamente!', 'success')
    else:
        flash('Error al eliminar el niño.', 'error')
    return redirect(url_for('gestionar_ninos'))

@app.route('/ninos/buscar', methods=['GET'])
def buscar_ninos():
    search_term = request.args.get('q', '')
    ninos = buscar_ninoBD(search_term)
    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/ninos/lista_ninos.html', ninos=ninos, dataLogin=dataLogin, search_term=search_term)

@app.route('/ninos/reporte-excel')
def reporte_ninos_excel():
    # Similar, puedes añadir verificación de sesión aquí
    # Esta función debería generar un archivo Excel y devolverlo como respuesta.
    # Necesitarías una función `generarReporteExcel_ninos()` que use una librería como pandas o openpyxl.
    flash('Funcionalidad de reporte Excel no implementada en este ejemplo.', 'info')
    return redirect(url_for('gestionar_ninos'))

# --- Otras rutas de tu aplicación (login, etc.) ---
# @app.route('/loginCliente')
# def loginCliente():
#     return "Página de login" # Reemplaza con tu lógica real de login




@app.route('/iniciar-actividad') # Este es el endpoint que el menú buscará
def iniciar_actividad(): # El nombre de esta función es el que usas en url_for('iniciar_actividad')
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        # Asegúrate que 'loginCliente' es el nombre correcto de tu función de login en router_login.py
        return redirect(url_for('loginCliente')) 

    # Si dataLoginSesion no está definida aquí, remueve la línea o impórtala
    dataLogin = { 
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    # Asegúrate que la ruta a tu plantilla es correcta:
    # 'public/iniciar_actividad.html' significa my-app/templates/public/iniciar_actividad.html
    return render_template('public/actividades/iniciar_actividad.html', dataLogin=dataLogin)

# --- Rutas para la gestión de Condiciones ---

@app.route('/condiciones')
def gestionar_condiciones():
    """
    Ruta para listar todas las condiciones.
    Recupera la lista completa de condiciones de la base de datos y la renderiza en la plantilla.
    """
    # Aquí puedes añadir una verificación de sesión si quieres que solo usuarios con rol específico vean esto
    # if 'conectado' not in session or session.get('rol') != 1: # Ejemplo de verificación de rol de administrador
    #     flash('Acceso denegado. No tienes permisos para gestionar condiciones.', 'error')
    #     return redirect(url_for('loginCliente'))
    
    condiciones = lista_condicionBD() 
    dataLogin = { # Simulación de dataLogin si la necesitas en la plantilla para el menú, etc.
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/condiciones/lista_condiciones.html', condiciones=condiciones, dataLogin=dataLogin)

@app.route('/condiciones/agregar', methods=['GET', 'POST'])
def agregar_condicion():
    """
    Ruta para agregar una nueva condición.
    Maneja el formulario de adición y guarda los datos en la base de datos.
    """
    # Similar, puedes añadir verificación de sesión aquí
    if request.method == 'POST':
        # Recopilar todos los campos del formulario
        nombre_condicion = request.form['nombre_condicion']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        
        resultado = guardar_condicionBD(nombre_condicion, descripcion, categoria)
        
        if resultado > 0:
            flash('Condición agregada exitosamente!', 'success')
            return redirect(url_for('gestionar_condiciones'))
        else:
            flash('Error al agregar la condición.', 'error')
    
    dataLogin = { 
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/condiciones/agregar_condicion.html', dataLogin=dataLogin)

@app.route('/condiciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_condicion(id):
    """
    Ruta para editar una condición existente.
    Recupera los datos de la condición por ID y maneja la actualización del formulario.
    """
    # Similar, puedes añadir verificación de sesión aquí
    condicion = obtener_condicion_por_idBD(id) 
    if not condicion:
        flash('Condición no encontrada.', 'error')
        return redirect(url_for('gestionar_condiciones'))

    if request.method == 'POST':
        # Recopilar todos los campos del formulario
        nombre_condicion = request.form['nombre_condicion']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        
        resultado = actualizar_condicionBD(id, nombre_condicion, descripcion, categoria)
        
        if resultado > 0:
            flash('Condición actualizada exitosamente!', 'success')
            return redirect(url_for('gestionar_condiciones'))
        else:
            flash('Error al actualizar la condición.', 'error')
            
    dataLogin = { 
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    # Pasar el objeto condicion completo a la plantilla para pre-llenar el formulario
    return render_template('public/condiciones/editar_condicion.html', condicion=condicion, dataLogin=dataLogin)

@app.route('/condiciones/eliminar/<int:id>')
def eliminar_condicion(id):
    """
    Ruta para eliminar una condición por su ID.
    """
    # Similar, puedes añadir verificación de sesión aquí
    resultado = eliminar_condicionBD(id)
    if resultado > 0:
        flash('Condición eliminada exitosamente!', 'success')
    else:
        flash('Error al eliminar la condición.', 'error')
    return redirect(url_for('gestionar_condiciones'))

@app.route('/condiciones/buscar', methods=['GET'])
def buscar_condiciones():
    """
    Ruta para buscar condiciones por un término de búsqueda (ej. nombre, descripción o categoría).
    """
    search_term = request.args.get('q', '')
    condiciones = buscar_condicionBD(search_term) 
    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/condiciones/lista_condiciones.html', condiciones=condiciones, dataLogin=dataLogin, search_term=search_term)

@app.route('/condiciones/reporte-excel')
def reporte_condiciones_excel():
    """
    Ruta para generar y descargar un reporte Excel de todas las condiciones.
    """
    # Similar, puedes añadir verificación de sesión aquí
    return generarReporteExcel_condiciones()

# --- Rutas para la gestión de Niño-Condiciones ---

@app.route("/nino-condiciones")
def gestionar_nino_condiciones():
    """
    Ruta para listar todas las relaciones niño-condición.
    """
    if "conectado" not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))
    
    # Obtener los datos de las condiciones de los niños
    nino_condiciones = lista_nino_condicionBD()
    
    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template("public/nino_condiciones/lista_nino_condiciones.html", 
                           nino_condiciones=nino_condiciones, 
                           dataLogin=dataLogin,
                           page_title='GESTIÓN DE CONDICIONES DE NIÑOS')

@app.route('/nino-condiciones/agregar', methods=['GET', 'POST'])
def agregar_nino_condicion():
    """
    Ruta para agregar una nueva relación niño-condición.
    """
    if "conectado" not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))

    if request.method == 'POST':
        datos = {
            "id_nino": request.form["id_nino"],
            "id_condicion": request.form["id_condicion"],
            "severidad": request.form["severidad"],
            "fecha_diagnostico": request.form["fecha_diagnostico"],
            "observaciones": request.form["observaciones"],
            "activo": 1 if "activo" in request.form else 0
        }
        resultado = insertar_nino_condicionBD(datos)
        if resultado > 0:
            flash("Condición agregada correctamente al niño!", "success")
            return redirect(url_for('gestionar_nino_condiciones'))
        else:
            flash("Error al agregar la condición al niño.", "error")
            
    # Para el método GET, cargar listas de niños y condiciones
    ninos = lista_ninoBD()
    condiciones = lista_condicionBD()
    
    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template("public/nino_condiciones/agregar_nino_condicion.html", 
                           ninos=ninos, 
                           condiciones=condiciones,
                           dataLogin=dataLogin,
                           page_title='AGREGAR CONDICIÓN A NIÑO')

@app.route('/nino-condiciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_nino_condicion(id):
    """
    Ruta para editar una relación niño-condición existente.
    """
    if "conectado" not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))

    nino_cond = obtener_nino_condicionBD(id)
    if not nino_cond:
        flash('Relación niño-condición no encontrada.', 'error')
        return redirect(url_for('gestionar_nino_condiciones'))

    if request.method == 'POST':
        datos = {
            "severidad": request.form["severidad"],
            "fecha_diagnostico": request.form["fecha_diagnostico"],
            "observaciones": request.form["observaciones"],
            "activo": 1 if "activo" in request.form else 0
        }
        resultado = actualizar_nino_condicionBD(id, datos)
        if resultado > 0:
            flash("Condición actualizada correctamente!", "success")
            return redirect(url_for('gestionar_nino_condiciones'))
        else:
            flash("Error al actualizar la condición.", "error")
            
    # Para el método GET, cargar listas de niños y condiciones para los dropdowns
    ninos = lista_ninoBD()
    condiciones = lista_condicionBD()

    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template("public/nino_condiciones/editar_nino_condicion.html", 
                           nino_cond=nino_cond, 
                           ninos=ninos, 
                           condiciones=condiciones,
                           dataLogin=dataLogin,
                           page_title='EDITAR CONDICIÓN DE NIÑO')

@app.route('/nino-condiciones/eliminar/<int:id>')
def eliminar_nino_condicion(id):
    """
    Ruta para eliminar una relación niño-condición.
    """
    if "conectado" not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))

    resultado = eliminar_nino_condicionBD(id)
    if resultado > 0:
        flash("Condición eliminada correctamente!", "warning")
    else:
        flash("Error al eliminar la condición.", "error")
    return redirect(url_for('gestionar_nino_condiciones'))

# NUEVA RUTA PARA EL REPORTE DE ACCESOS
@app.route('/reportes/accesos')
def reportes_accesos():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))
    
    # Obtener los datos de acceso
    accesos = accesosReporte()
    
    dataLogin = {
        "id": session.get("id"),
        "rol": session.get("rol"),
    }
    return render_template('public/reportes/lista_accesos.html', 
                           accesos=accesos, 
                           dataLogin=dataLogin,
                           page_title='REPORTE DE ACCESOS')

@app.route('/reportes/accesos/excel')
def descargar_reporte_accesos_excel():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginCliente'))
    
    return generarReporteExcel()

@app.route('/usuarios/buscar', methods=['GET'])
def buscar_usuarios():
    search_term = request.args.get('q', '')
    usuarios = buscar_usuariosBD(search_term)

    return render_template(
        'public/usuarios/lista_usuarios.html',
        resp_usuariosBD=usuarios,
        search_term=search_term,
        dataLogin=dataLoginSesion(),  # Asume que esta función existe
        areas=lista_areasBD(),
        roles=lista_rolesBD()
    )


@app.route('/borrar-area/<string:id_area>/', methods=['GET'])
def borrarArea(id_area):
    resp = eliminarArea(id_area)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_areas'))
    else:
        flash('Hay usuarios que pertenecen a esta área', 'error')
        return redirect(url_for('lista_areas'))


@app.route("/descargar-informe-accesos/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route("/reporte-accesos", methods=['GET'])
def reporteAccesos():
    if 'conectado' in session:
        userData = dataLoginSesion()
        return render_template('public/perfil/reportes.html',  reportes=dataReportes(),lastAccess=lastAccessBD(userData.get('cedula')), dataLogin=dataLoginSesion())


#CREAR AREA
@app.route('/crear-area', methods=['POST'])
def crearArea():
    if request.method == 'POST':
        nombre_area = request.form['nombre_area']
        descripcion = request.form['descripcion'] # <-- ¡Ahora sí obtén la descripción!

        # Asegúrate de que tu función 'guardarArea' acepte la descripción
        resultado_insert = guardarArea(nombre_area, descripcion) # <-- Pasa la descripción

        if resultado_insert:
            flash('El Área fue creada correctamente', 'success')
            return redirect(url_for('lista_areas'))
        else:
            flash('Hubo un error al guardar el área.', 'danger') # Mensaje flash consistente
            return redirect(url_for('lista_areas')) # Siempre redirige después de enviar un formulario
    # Si la petición no es POST, muestra el formulario de creación
    return render_template('public/usuarios/lista_areas.html')

@app.route('/actualizar-area', methods=['POST'])
def updateArea():
    if request.method == 'POST':
        nombre_area = request.form['nombre_area']
        id_area = request.form['id_area']
        descripcion = request.form['descripcion'] # <-- ¡Obtén la descripción aquí!

        # Asegúrate de que tu función 'actualizarArea' acepte la descripción
        resultado_update = actualizarArea(id_area, nombre_area, descripcion) # <-- Pasa la descripción

        if resultado_update:
            flash('El área fue actualizada correctamente', 'success') # Mensaje corregido y claro
        else:
            flash('Hubo un error al actualizar el área. Por favor, verifica los logs.', 'danger')

        return redirect(url_for('lista_areas'))

    # Si no es un POST, o si se accede directamente
    return redirect(url_for('lista_areas'))
