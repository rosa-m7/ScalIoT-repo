print('*** router_analitica.py CARGADO', flush=True)
from flask import Blueprint, jsonify, request, current_app
from firebase_admin import db
from datetime import datetime

bp_analitica = Blueprint('bp_analitica', __name__)

# --- Helper Functions ---

def timestamp_to_date(ts):
    """Converts a string timestamp 'YYYY-MM-DD_HH-MM-SS' to a datetime object."""
    try:
        return datetime.strptime(ts, '%Y-%m-%d_%H-%M-%S')
    except (ValueError, TypeError):
        return None

# --- Text-based Report Generation Functions (for Evaluation Mode) ---

def interpretar_velocidad(segundos):
    if segundos < 15:
        return "verde - buena coordinacion y tiempo de reaccion"
    elif 15 <= segundos <= 25:
        return "amarillo - coordinacion promedio, posible distraccion"
    else:
        return "rojo - posible lentitud motora, inseguridad o baja atencion"

def interpretar_precision(porcentaje):
    if porcentaje > 70:
        return "verde - alta precision motora y comprension de instrucciones"
    elif 40 <= porcentaje <= 70:
        return "amarillo - desempeno intermitente o dificultad en mantener foco"
    else:
        return "rojo - dificultades motrices, baja comprension o desatencion persistente"

def interpretar_resistencia(minutos):
    if minutos >= 5:
        return "verde - buena resistencia fisica y atencion"
    else:
        return "rojo - fatiga temprana, frustracion o poca tolerancia al esfuerzo"

def analizar_regularidad(lista_ordenes):
    if len(lista_ordenes) < 4:
        return "no hay suficientes datos para analizar la regularidad"
    tendencia = []
    for i in range(1, len(lista_ordenes)):
        if lista_ordenes[i][1] and not lista_ordenes[i-1][1]:
            tendencia.append("mejora")
        elif not lista_ordenes[i][1] and lista_ordenes[i-1][1]:
            tendencia.append("decae")
    
    if tendencia.count("mejora") > tendencia.count("decae"):
        return "adaptacion tardia: mejora durante la sesion"
    elif tendencia.count("decae") > tendencia.count("mejora"):
        return "fatiga o problemas de atencion sostenida"
    else:
        return "rendimiento estable o inconsistente"

def _generar_informe_desde_data(modo_eval_data):
    """Helper to generate the text report from evaluation data."""
    res = modo_eval_data.get("resultados_evaluacion", {})
    tiempo_total = res.get("tiempo_total", 0)
    inicio_sesion = modo_eval_data.get("inicio_sesion")
    fin_sesion = modo_eval_data.get("fin_sesion")
    
    total_ordenes = res.get("total_ordenes", 0)
    correctas = res.get("respuestas_correctas", 0)
    tiempo_prom = tiempo_total / total_ordenes if total_ordenes else 0
    precision = (correctas / total_ordenes) * 100 if total_ordenes else 0
    
    botones = modo_eval_data.get("botones", {})
    escalones = modo_eval_data.get("escalones", {})
    bot_correctos = sum(1 for b in botones.values() if b.get("correcta") is True)
    bot_total = len(botones)
    esc_correctos = sum(1 for e in escalones.values() if e.get("correcta") is True)
    esc_total = len(escalones)
    bot_precision = (bot_correctos / bot_total) * 100 if bot_total > 0 else 0
    esc_precision = (esc_correctos / esc_total) * 100 if esc_total > 0 else 0
    
    duracion_min = 0
    if inicio_sesion and fin_sesion:
        try:
            t1 = timestamp_to_date(inicio_sesion)
            t2 = timestamp_to_date(fin_sesion)
            if t1 and t2:
                duracion_min = (t2 - t1).total_seconds() / 60
            else:
                duracion_min = tiempo_total / 60
        except (ValueError, TypeError):
            duracion_min = tiempo_total / 60
    else:
        duracion_min = tiempo_total / 60

    motricidad_informe = f"Botones: {bot_precision:.1f}% acierto | Escalones: {esc_precision:.1f}% acierto"
    if bot_precision > esc_precision:
        motricidad_informe += " - Mejor rendimiento en botones"
    elif esc_precision > bot_precision:
        motricidad_informe += " - Mejor rendimiento en escalones"

    ordenes = sorted([(d.get("orden_numero", 0), d.get("correcta", False)) for d in list(botones.values()) + list(escalones.values())])

    # Diagnóstico automático útil incluso con pocos datos
    if total_ordenes == 0:
        return {
            'informe': 'No hay suficientes datos para un análisis detallado. La sesión fue muy corta o no se registraron respuestas. Se recomienda realizar una nueva evaluación para obtener un diagnóstico confiable.'
        }
    if total_ordenes < 4:
        return {
            'informe': f"Sesión breve con solo {total_ordenes} respuestas. Precisión: {precision:.1f}%. Motricidad: {'alta' if precision > 70 else 'media' if precision > 40 else 'baja'}. Se recomienda más práctica para un análisis confiable."
        }
    # Análisis global según precisión y velocidad
    nivel_motricidad = 'alta' if precision > 80 else 'media' if precision > 50 else 'baja'
    velocidad_txt = interpretar_velocidad(tiempo_prom)
    precision_txt = interpretar_precision(precision)
    regularidad_txt = analizar_regularidad(ordenes)
    resistencia_txt = interpretar_resistencia(duracion_min)
    informe = (
        f"Motricidad {nivel_motricidad}. "
        f"Precisión: {precision:.1f}% ({precision_txt}). "
        f"Velocidad: {tiempo_prom:.2f} seg/orden ({velocidad_txt}). "
        f"Duración: {duracion_min:.2f} min ({resistencia_txt}). "
        f"Regularidad: {regularidad_txt}."
    )
    return {
        'informe': informe
    }

# --- ENDPOINTS FOR GENERAL ANALYTICS (AGRUPADOS POR DÍA) ---

@bp_analitica.route('/api/fechas_sesiones_general', methods=['GET'])
def fechas_sesiones_general():
    """Devuelve una lista de fechas únicas (YYYY-MM-DD) de todas las sesiones registradas."""
    try:
        ref_sesiones = db.reference('sesiones')
        sesiones = ref_sesiones.get(shallow=True)
        fechas = set()
        if sesiones:
            for ts in sesiones.keys():
                if len(ts) >= 10:
                    fechas.add(ts[:10])
        fechas_ordenadas = sorted(list(fechas), reverse=True)
        return jsonify(fechas_ordenadas)
    except Exception as e:
        current_app.logger.error(f"Error obteniendo fechas de sesiones generales: {e}")
        return jsonify({'error': str(e)}), 500

@bp_analitica.route('/api/datos_sesion_filtrada', methods=['GET'])
def datos_sesion_filtrada():
    """Devuelve datos agregados por día y modo para analítica general."""
    fecha = request.args.get('fecha')  # formato YYYY-MM-DD
    modo = request.args.get('modo')    # 'modoevaluacion', 'modojuego', 'mododescanso'
    if not fecha or not modo:
        return jsonify({'error': 'Faltan parámetros: fecha o modo'}), 400
    if modo == 'mododescanso':
        return jsonify({'error': 'El modo Descanso no tiene activaciones para mostrar.'}), 400
    try:
        ref_sesiones = db.reference('sesiones')
        sesiones = ref_sesiones.get()
        if not sesiones:
            return jsonify({'error': 'No hay sesiones registradas'}), 404
        # Filtrar sesiones por día
        sesiones_del_dia = [s for k, s in sesiones.items() if k.startswith(fecha)]
        total_activaciones = 0
        colores_botones = {}
        colores_escalones = {}
        for sesion in sesiones_del_dia:
            modo_data = sesion.get(modo)
            if not modo_data:
                continue
            # Botones
            botones = modo_data.get('botones', {})
            for b in botones.values():
                color = b.get('color', 'Sin color')
                colores_botones[color] = colores_botones.get(color, 0) + (1 if b.get('correcta') is not False else 0)
                total_activaciones += (1 if b.get('correcta') is not False else 0)
            # Escalones
            escalones = modo_data.get('escalones', {})
            for e in escalones.values():
                color = e.get('color', 'Sin color')
                colores_escalones[color] = colores_escalones.get(color, 0) + (1 if e.get('correcta') is not False else 0)
                total_activaciones += (1 if e.get('correcta') is not False else 0)
        return jsonify({
            'total_activaciones': total_activaciones,
            'colores_botones': colores_botones,
            'colores_escalones': colores_escalones
        })
    except Exception as e:
        current_app.logger.error(f"Error en datos_sesion_filtrada: {e}")
        return jsonify({'error': str(e)}), 500

# --- ENDPOINTS FOR CHILD-SPECIFIC ANALYTICS ---

@bp_analitica.route('/api/fechas_sesiones/<nino_id>', methods=['GET'])
def get_fechas_sesiones_por_nino(nino_id):
    """
    Returns a sorted list of unique session timestamps for a given child.
    This is used to populate the session selector dropdown.
    """
    try:
        # 1. Get session timestamps associated with the child
        ref_nino_sesiones = db.reference(f'ninos/{nino_id}/sesiones')
        sesiones_nino_keys = ref_nino_sesiones.get(shallow=True)

        if not sesiones_nino_keys:
            return jsonify([]) # No sessions associated with the child

        # 2. Get all session timestamps from the global sessions collection
        ref_sesiones_global = db.reference('sesiones')
        sesiones_global_keys = ref_sesiones_global.get(shallow=True)

        if not sesiones_global_keys:
            return jsonify([]) # No sessions in the global collection

        # 3. Buscar coincidencias exactas y por minuto
        from datetime import datetime, timedelta
        sesiones_nino = list(sesiones_nino_keys.keys())
        sesiones_global = set(sesiones_global_keys.keys())
        coincidencias = []
        for ts_nino in sesiones_nino:
            # Exacto
            if ts_nino in sesiones_global:
                # Verifica que haya datos en la raíz sesiones
                sesion_data = db.reference(f'sesiones/{ts_nino}').get()
                if sesion_data:
                    coincidencias.append({'ts_nino': ts_nino, 'ts_global': ts_nino})
                continue
            # Por minuto
            ts_min = ts_nino[:16] if len(ts_nino) > 16 else ts_nino
            match_min = next((ts for ts in sesiones_global if ts.startswith(ts_min)), None)
            if match_min:
                sesion_data = db.reference(f'sesiones/{match_min}').get()
                if sesion_data:
                    coincidencias.append({'ts_nino': ts_nino, 'ts_global': match_min})
                continue
            # Minuto anterior
            try:
                dt = datetime.strptime(ts_min, '%Y-%m-%d_%H-%M')
                dt_prev = dt - timedelta(minutes=1)
                ts_prev = dt_prev.strftime('%Y-%m-%d_%H-%M')
                match_prev = next((ts for ts in sesiones_global if ts.startswith(ts_prev)), None)
                if match_prev:
                    sesion_data = db.reference(f'sesiones/{match_prev}').get()
                    if sesion_data:
                        coincidencias.append({'ts_nino': ts_nino, 'ts_global': match_prev})
                    continue
            except Exception:
                pass
        # 4. Return the sorted list of objects (newest first by ts_global)
        timestamps_ordenados = sorted(coincidencias, key=lambda x: x['ts_global'], reverse=True)
        return jsonify(timestamps_ordenados)

    except Exception as e:
        current_app.logger.error(f"Error getting session dates for child {nino_id}: {e}")
        return jsonify({'error': str(e)}), 500

@bp_analitica.route('/api/datos_graficas_sesion', methods=['GET'])
def get_datos_graficas_sesion():
    """
    Returns structured data for a specific session, ready for graphing.
    Returns an object with keys for each mode: evaluacion, juego, descanso (even if empty).
    """
    try:
        session_ts = request.args.get('session_ts')
        nino_id = request.args.get('nino_id')

        if not session_ts or not nino_id:
            return jsonify({'error': 'Faltan parámetros: session_ts o nino_id'}), 400

        # 1. Verify that the session belongs to the child
        # Buscar sesión exacta o por minuto
        def buscar_sesion_por_minuto(nino_id, session_ts):
            """Devuelve el timestamp encontrado y el ref, o (None, None) si no existe."""
            ref = db.reference(f'ninos/{nino_id}/sesiones/{session_ts}')
            if ref.get():
                return session_ts, ref
            # Intentar truncar a minutos
            try:
                if len(session_ts) > 16:
                    ts_min = session_ts[:16]  # 'YYYY-MM-DD_HH-MM'
                else:
                    ts_min = session_ts
                ref_min = db.reference(f'ninos/{nino_id}/sesiones/{ts_min}')
                if ref_min.get():
                    return ts_min, ref_min
                # Intentar con el minuto anterior
                from datetime import datetime, timedelta
                dt = datetime.strptime(ts_min, '%Y-%m-%d_%H-%M')
                dt_prev = dt - timedelta(minutes=1)
                ts_prev = dt_prev.strftime('%Y-%m-%d_%H-%M')
                ref_prev = db.reference(f'ninos/{nino_id}/sesiones/{ts_prev}')
                if ref_prev.get():
                    return ts_prev, ref_prev
            except Exception as e:
                pass
            return None, None
        ts_encontrado, nino_sesion_ref = buscar_sesion_por_minuto(nino_id, session_ts)
        if not nino_sesion_ref:
            # Buscar en ninos/<nino_id>/sesiones alguna variante por minuto
            ref_nino_sesiones = db.reference(f'ninos/{nino_id}/sesiones')
            sesiones_nino_keys = list((ref_nino_sesiones.get(shallow=True) or {}).keys())
            ts_min = session_ts[:16] if len(session_ts) > 16 else session_ts
            match_min = next((ts for ts in sesiones_nino_keys if ts.startswith(ts_min)), None)
            if match_min:
                # Permite la consulta aunque los segundos sean diferentes
                nino_sesion_ref = db.reference(f'ninos/{nino_id}/sesiones/{match_min}')
            else:
                from datetime import datetime, timedelta
                try:
                    dt = datetime.strptime(ts_min, '%Y-%m-%d_%H-%M')
                    dt_prev = dt - timedelta(minutes=1)
                    ts_prev = dt_prev.strftime('%Y-%m-%d_%H-%M')
                    match_prev = next((ts for ts in sesiones_nino_keys if ts.startswith(ts_prev)), None)
                    if match_prev:
                        nino_sesion_ref = db.reference(f'ninos/{nino_id}/sesiones/{match_prev}')
                except Exception:
                    pass
            if not nino_sesion_ref:
                # Validar si el session_ts global existe y tiene datos, y hay una sesión del niño en el mismo minuto
                ref_global_sesion = db.reference(f'sesiones/{session_ts}')
                global_data = ref_global_sesion.get()
                if global_data and any(ts.startswith(ts_min) for ts in sesiones_nino_keys):
                    # Permitir la consulta aunque el niño tenga segundos diferentes
                    pass
                else:
                    return jsonify({'error': f'No se encontró la sesión (ni por minuto) para el niño {nino_id}.'}), 403
        else:
            session_ts = ts_encontrado

        # 2. Get the session data
        sesion_ref = db.reference(f'sesiones/{session_ts}')
        sesion = sesion_ref.get()

        if not sesion:
            return jsonify({'error': f'No se encontró la sesión con timestamp {session_ts}'}), 404

        # --- NUEVO: preparar los tres modos ---
        response = {'evaluacion': None, 'juego': None, 'descanso': None}

        # --- Evaluacion ---
        modo_eval = sesion.get('modoevaluacion')
        resultados_eval = None
        if modo_eval:
            if 'resultados_evaluacion' in modo_eval:
                resultados_eval = modo_eval.get('resultados_evaluacion', {})
            elif 'resultados_evaluacion' in sesion:
                resultados_eval = sesion.get('resultados_evaluacion', {})
            else:
                resultados_eval = None
            if resultados_eval:
                botones = modo_eval.get('botones', {})
                escalones = modo_eval.get('escalones', {})
                response['evaluacion'] = {
                    'botones_data': {
                        'activados': sum(1 for b in botones.values() if b.get('correcta') is True),
                        'no_activados': sum(1 for b in botones.values() if b.get('correcta') is False)
                    },
                    'escalones_data': {
                        'activados': sum(1 for e in escalones.values() if e.get('correcta') is True),
                        'no_activados': sum(1 for e in escalones.values() if e.get('correcta') is False)
                    },
                    'resultados_data': {
                        'aciertos': resultados_eval.get('respuestas_correctas', 0),
                        'desaciertos': resultados_eval.get('respuestas_incorrectas', 0)
                    },
                    'inicio_sesion': modo_eval.get('inicio_sesion'),
                    'fin_sesion': modo_eval.get('fin_sesion'),
                    'inicio': modo_eval.get('inicio'),
                    'fin': modo_eval.get('fin'),
                    'tiempo_total': resultados_eval.get('tiempo_total', 0)
                }
            else:
                response['evaluacion'] = {'mensaje': 'No hay datos de resultados en este modo.'}
        else:
            response['evaluacion'] = {'mensaje': 'No hay datos de evaluación para esta sesión.'}

        # --- Juego ---
        modo_juego = sesion.get('modojuego')
        if modo_juego:
            response['juego'] = modo_juego
        else:
            response['juego'] = {'mensaje': 'No hay datos de juego para esta sesión.'}

        # --- Descanso ---
        modo_descanso = sesion.get('mododescanso')
        if modo_descanso:
            response['descanso'] = modo_descanso
        else:
            response['descanso'] = {'mensaje': 'No hay datos de descanso para esta sesión.'}

        # --- Diagnóstico general (si existe) ---
        if 'diagnostico' in sesion:
            response['diagnostico'] = sesion['diagnostico']
        else:
            response['diagnostico'] = ''

        return jsonify(response)

    except Exception as e:
        current_app.logger.error(f"Error in get_datos_graficas_sesion: {e}")
        return jsonify({'error': str(e)}), 500

@bp_analitica.route('/api/guardar_diagnostico_sesion', methods=['POST'])
def guardar_diagnostico_sesion():
    try:
        data = request.get_json()
        nino_id = data.get('nino_id')
        session_ts = data.get('session_ts')
        diagnostico = (data.get('diagnostico') or '').strip()[:200]
        if not nino_id or not session_ts:
            return jsonify({'error': 'Faltan parámetros: nino_id o session_ts'}), 400
        if not diagnostico:
            return jsonify({'error': 'El diagnóstico no puede estar vacío'}), 400

        # Verifica que la sesión pertenezca al niño
        # Buscar sesión exacta o por minuto
        def buscar_sesion_por_minuto(nino_id, session_ts):
            """Devuelve el timestamp encontrado y el ref, o (None, None) si no existe."""
            ref = db.reference(f'ninos/{nino_id}/sesiones/{session_ts}')
            if ref.get():
                return session_ts, ref
            # Intentar truncar a minutos
            try:
                if len(session_ts) > 16:
                    ts_min = session_ts[:16]  # 'YYYY-MM-DD_HH-MM'
                else:
                    ts_min = session_ts
                ref_min = db.reference(f'ninos/{nino_id}/sesiones/{ts_min}')
                if ref_min.get():
                    return ts_min, ref_min
                # Intentar con el minuto anterior
                from datetime import datetime, timedelta
                dt = datetime.strptime(ts_min, '%Y-%m-%d_%H-%M')
                dt_prev = dt - timedelta(minutes=1)
                ts_prev = dt_prev.strftime('%Y-%m-%d_%H-%M')
                ref_prev = db.reference(f'ninos/{nino_id}/sesiones/{ts_prev}')
                if ref_prev.get():
                    return ts_prev, ref_prev
            except Exception as e:
                pass
            return None, None
        ts_encontrado, nino_sesion_ref = buscar_sesion_por_minuto(nino_id, session_ts)
        if not nino_sesion_ref:
            return jsonify({'error': f'No se encontró la sesión (ni por minuto) para el niño {nino_id}.'}), 403
        session_ts = ts_encontrado

        # Guarda el diagnóstico en la sesión
        sesion_ref = db.reference(f'sesiones/{session_ts}')
        sesion_ref.update({'diagnostico': diagnostico})
        return jsonify({'success': True})
    except Exception as e:
        current_app.logger.error(f"Error en guardar_diagnostico_sesion: {e}")
        return jsonify({'error': str(e)}), 500

@bp_analitica.route('/api/informe_sesion_nino', methods=['GET'])
def get_informe_sesion_nino():
    """
    Generates a text-based interpretive report for an 'evaluation' mode session.
    """
    try:
        session_ts = request.args.get('session_ts')
        if not session_ts:
            return jsonify({'error': 'Falta el timestamp de la sesión'}), 400

        sesion_ref = db.reference(f'sesiones/{session_ts}')
        sesion = sesion_ref.get()
        
        if not sesion or 'modoevaluacion' not in sesion:
            return jsonify({'informe': 'No aplica', 'mensaje': 'No es una sesión de evaluación válida.'})
        
        modo_eval_data = sesion.get("modoevaluacion")
        if "resultados_evaluacion" not in modo_eval_data:
            return jsonify({'informe': 'No hay suficientes datos para generar un análisis interpretativo de la sesión. Se recomienda realizar una evaluación más completa.'})

        informe = _generar_informe_desde_data(modo_eval_data)
        return jsonify(informe)

    except Exception as e:
        current_app.logger.error(f"Error in get_informe_sesion_nino: {e}")
        return jsonify({'error': str(e)}), 500
