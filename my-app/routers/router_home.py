
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify, send_file #Se agrego solo send_file
from controllers.funciones_login import *
from app import app # Si 'app' ya se inicializa con Flask(__name__) en 'app.py', esta línea podría ser redundante o generar un error si no se maneja bien la inicialización.
from mysql.connector.errors import Error
# Importando cenexión a BD
from controllers.funciones_home import *
# Se importa esta linea nueva para las consultas
import pandas as pd

@app.route('/lista-de-areas', methods=['GET'])
def lista_areas():
    if 'conectado' in session:
        return render_template('public/usuarios/lista_areas.html', areas=lista_areasBD(), dataLogin=dataLoginSesion())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        return render_template('public/usuarios/lista_usuarios.html',  resp_usuariosBD=lista_usuariosBD(), dataLogin=dataLoginSesion(), roles=lista_rolesBD())
    else:
        return redirect(url_for('inicioCpanel'))

@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))
    else:
        # If resp is False, it means the user was not deleted.
        # You should flash an error message and redirect.
        flash('No se pudo eliminar el usuario o el usuario no existe.', 'danger')
        return redirect(url_for('usuarios')) # Redirect back to the user list or an appropriate page
    

# ----------------- RUTAS PARA GRÁFICAS DE NIÑOS ------------------

from firebase_admin import db

@app.route('/obtener_ninos')
def obtener_ninos():
    try:
        ninos = lista_ninoBD()
        ninos_activos = [n for n in ninos if n['activo'] == 1]
        return jsonify({"ninos": [{"id": n["id_nino"], "nombre": f'{n["nombre"]} {n["apellido"]}'} for n in ninos_activos]})
    except Exception as e:
        print(f"Error en /obtener_ninos: {e}")
        return jsonify({"error": "No se pudieron obtener los niños"}), 500


@app.route('/analisis_nino')
def analisis_nino():
    try:
        id_nino = request.args.get('id_nino')
        nino = obtener_nino_por_idBD(id_nino)
        if not nino:
            return jsonify({"error": "Niño no encontrado"}), 404

        codigo_nino = nino["codigo_nino"]

        # Obtener las sesiones asociadas al código del niño en Firebase
        sesiones_ref = db.reference(f"ninos/{codigo_nino}/sesiones")
        sesiones_ids = sesiones_ref.get()

        if not sesiones_ids:
            return jsonify([])

        datos = []
        for sesion_id in sesiones_ids:
            resultados_ref = db.reference(f"sesiones/{sesion_id}/resultados_evaluacion")
            resultados = resultados_ref.get()
            if resultados:
                datos.append({
                    "sesion_id": sesion_id,
                    "resultados": resultados
                })

        return jsonify(datos)

    except Exception as e:
        print(f"Error en /analisis_nino: {e}")
        return jsonify({"error": "Error interno al obtener análisis del niño"}), 500




#Se agrega las siguientes lineas
@app.route('/api/sessions', methods=['GET'])
def api_get_sessions():
    """Endpoint para obtener la lista de sesiones disponibles de Firebase."""
    try:
        # Llama a la función desde funciones_home.py
        sessions = get_session_types()
        return jsonify(sessions), 200
    except Exception as e:
        print(f"Error en /api/sessions: {e}") # Para depuración
        return jsonify({"error": "Error interno del servidor al obtener sesiones.", "details": str(e)}), 500

@app.route('/api/session_modes/<session_date>', methods=['GET'])
def api_get_session_modes(session_date):
    """Endpoint para obtener los modos disponibles para una fecha específica en Firebase."""
    try:
        from controllers.funciones_home import get_modes_for_date
        modos = get_modes_for_date(session_date)
        return jsonify(modos), 200
    except Exception as e:
        print(f"Error en /api/session_modes/{session_date}: {e}")
        return jsonify({"error": "Error interno del servidor al obtener modos.", "details": str(e)}), 500

@app.route('/api/session_dates/<session_name>', methods=['GET'])
def api_get_session_dates(session_name):
    """Endpoint para obtener las fechas disponibles para una sesión específica de Firebase."""
    try:
        # Llama a la función desde funciones_home.py
        dates = get_session_dates(session_name)
        return jsonify(dates), 200
    except Exception as e:
        print(f"Error en /api/session_dates/{session_name}: {e}") # Para depuración
        return jsonify({"error": "Error interno del servidor al obtener fechas.", "details": str(e)}), 500

@app.route('/api/generate_report', methods=['POST'])
def api_generate_report():
    """Endpoint para generar y descargar el reporte Excel de Firebase."""
    data = request.get_json()
    session_type = data.get('session_type')
    session_date = data.get('session_date')

    if not session_type or not session_date:
        return jsonify({'error': "Parámetros 'session_type' y 'session_date' son requeridos."}), 400

    try:
        # Llama a la función principal de generación de reporte de Firebase
        # que ahora está en funciones_home.py
        file_buffer, file_name = generar_reporte_firebase(session_type, session_date)
        
        return send_file(
            file_buffer, 
            as_attachment=True,
            download_name=file_name, # Usa el nombre de archivo generado por la función
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}") # Para depuración
        return jsonify({"error": str(fnfe)}), 500
    except ValueError as ve: # Captura errores de datos específicos de la función
        print(f"Error de datos al generar reporte: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error inesperado al generar reporte: {e}") # Para depuración
        return jsonify({"error": "Error interno del servidor al generar el reporte.", "details": str(e)}), 500
#Hasta aqui

@app.route('/instrucciones')
def instrucciones():
    return render_template('public/instrucciones.html')


# Se agregaron estas líneas
@app.route('/api/chart_data_nino/<int:nino_id>', methods=['GET'])
def api_get_chart_data_nino(nino_id):
    try:
        chart_data = get_chart_data_for_nino(nino_id)
        return jsonify(chart_data), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        print(f"Error en /api/chart_data_nino: {e}")
        return jsonify({"error": "Error interno del servidor al obtener datos para gráficos del niño."}), 500

@app.route('/api/chart_data', methods=['GET'])
def api_get_chart_data():
    """
    Endpoint para obtener los datos necesarios para generar los gráficos
    de botones y escalones en el frontend.
    """
    session_type = request.args.get('session_type')
    session_date = request.args.get('session_date')

    if not session_type or not session_date:
        return jsonify({'error': "Parámetros 'session_type' y 'session_date' son requeridos."}), 400

    try:
        chart_data = get_firebase_chart_data(session_type, session_date)
        return jsonify(chart_data), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        print(f"Error en /api/chart_data: {e}")
        return jsonify({"error": "Error interno del servidor al obtener datos para gráficos.", "details": str(e)}), 500
# Hasta aqui
# ============================================
# RUTAS DE CONTROL DE SESIÓN Y MODO
# ============================================

@app.route('/api/sesion/estado', methods=['GET'])
def api_sesion_estado():
    """Obtiene el estado actual de la sesión"""
    try:
        ref = db.reference('estado/sesion')
        sesion = ref.get()
        
        if sesion is None:
            return jsonify({
                'activa': 0,
                'modo': 'ninguno',
                'mensaje': 'Sistema desactivado'
            }), 200
        
        return jsonify({
            'activa': sesion.get('activa', 0),
            'modo': sesion.get('modo', 'ninguno'),
            'id_nino': sesion.get('id_nino', ''),
            'mensaje': 'Estado obtenido correctamente'
        }), 200
        
    except Exception as e:
        print(f"Error al obtener el estado de la sesión: {e}")
        return jsonify({
            'activa': 0,
            'modo': 'ninguno',
            'error': str(e)
        }), 500


@app.route('/api/modo/estado', methods=['GET'])
def api_modo_estado():
    """Obtiene el modo actual del sistema"""
    try:
        ref = db.reference('estado/modo')
        modo_data = ref.get()
        
        if modo_data is None:
            return jsonify({
                'modo': 'ninguno',
                'mensaje': 'Sin modo activo'
            }), 200
        
        if isinstance(modo_data, str):
            modo = modo_data
        else:
            modo = modo_data.get('actual', 'ninguno') if isinstance(modo_data, dict) else 'ninguno'
        
        return jsonify({
            'modo': modo,
            'mensaje': 'Modo obtenido correctamente'
        }), 200
        
    except Exception as e:
        print(f"Error al obtener el estado del modo: {e}")
        return jsonify({
            'modo': 'ninguno',
            'error': str(e)
        }), 500


@app.route('/api/modo/actualizar', methods=['POST'])
def api_modo_actualizar():
    """Actualiza el modo del sistema"""
    try:
        from datetime import datetime
        data = request.get_json()
        nuevo_modo = data.get('modo', '').lower()
        
        modos_validos = ['evaluacion', 'juego', 'descanso', 'ninguno']
        if nuevo_modo not in modos_validos:
            return jsonify({
                'error': f'Modo inválido. Debe ser: {", ".join(modos_validos)}'
            }), 400
        
        ref = db.reference('estado/modo')
        ref.set({
            'actual': nuevo_modo,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': f'Modo cambiado a {nuevo_modo}',
            'modo': nuevo_modo
        }), 200
        
    except Exception as e:
        print(f"Error al actualizar modo: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/sesion/iniciar', methods=['POST'])
def api_sesion_iniciar():
    """Inicia una sesión nueva"""
    try:
        from datetime import datetime
        data = request.get_json()
        id_nino = data.get('id_nino', '')
        
        timestamp = datetime.now().isoformat()
        
        ref = db.reference('estado/sesion')
        ref.set({
            'activa': 1,
            'id_nino': id_nino,
            'fecha_inicio': timestamp,
            'modo': 'evaluacion'
        })
        
        return jsonify({
            'success': True,
            'message': 'Sistema activado correctamente'
        }), 200
        
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/sesion/finalizar', methods=['POST'])
def api_sesion_finalizar():
    """Finaliza la sesión actual"""
    try:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        ref = db.reference('estado/sesion')
        ref.set({
            'activa': 0,
            'fecha_fin': timestamp,
            'modo': 'ninguno'
        })
        
        return jsonify({
            'success': True,
            'message': 'Sistema desactivado correctamente'
        }), 200
        
    except Exception as e:
        print(f"Error al finalizar sesión: {e}")
        return jsonify({
            'error': str(e)
        }), 500

