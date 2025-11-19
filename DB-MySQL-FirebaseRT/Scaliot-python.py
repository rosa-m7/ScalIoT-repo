# -- coding: utf-8 --
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import paho.mqtt.client as mqtt
import time
import signal
import sys
import threading
import json
import subprocess
import queue
import random
import pygame
from pydub import AudioSegment
import tempfile
import os

# ---------- AudioManager: Reproducción local con pitch, loop y mute selectivo ----------
class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_thread = None
        self.bg_stop_event = threading.Event()
        self.bg_muted = False
        self.bg_volume = 0.6
        self.sfx_muted = False
        self.lock = threading.Lock()

    def set_volume(self, volume):  # 0-100
        with self.lock:
            pygame.mixer.music.set_volume(volume / 100.0)
            self.bg_volume = volume / 100.0

    def play_sound(self, filepath, pitch=1.0):
        if self.sfx_muted:
            return
        def _worker():
            if pitch != 1.0:
                sound = AudioSegment.from_file(filepath)
                new_sound = sound._spawn(sound.raw_data, overrides={
                    "frame_rate": int(sound.frame_rate * pitch)
                }).set_frame_rate(sound.frame_rate)
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tf:
                    new_sound.export(tf.name, format="wav")
                    temp_path = tf.name
                s = pygame.mixer.Sound(temp_path)
                s.play()
                while pygame.mixer.get_busy():
                    pygame.time.wait(50)
                os.remove(temp_path)
            else:
                s = pygame.mixer.Sound(filepath)
                s.play()
                while pygame.mixer.get_busy():
                    pygame.time.wait(50)
        threading.Thread(target=_worker, daemon=True).start()

    def play_background(self, filepath, loop=True):
        with self.lock:
            self.bg_stop_event.set()
            if self.background_thread and self.background_thread.is_alive():
                self.background_thread.join()
            self.bg_stop_event.clear()
            def _bg():
                while not self.bg_stop_event.is_set():
                    if not self.bg_muted:
                        pygame.mixer.music.load(filepath)
                        pygame.mixer.music.set_volume(self.bg_volume)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy() and not self.bg_stop_event.is_set():
                            pygame.time.wait(200)
                    else:
                        pygame.time.wait(500)
                    if not loop:
                        break
            self.background_thread = threading.Thread(target=_bg, daemon=True)
            self.background_thread.start()

    def mute_background(self, mute=True):
        with self.lock:
            self.bg_muted = mute
            if mute:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.bg_volume)

    def mute_sfx(self, mute=True):
        with self.lock:
            self.sfx_muted = mute

    def stop_background(self):
        with self.lock:
            self.bg_stop_event.set()
            pygame.mixer.music.stop()

    def quit(self):
        self.stop_background()
        pygame.mixer.quit()

# ------------- UnifiedController con AudioManager -----------------
class UnifiedController:
    def __init__(self):
        self.sesion_id_global = None
        self.sistema_activo = False
        self.modo_actual = None
        self.modo_detectado = None
        self.ultimo_cambio_sistema = 0
        self.TIEMPO_MINIMO_ENTRE_CAMBIOS = 2

        self.audio_enabled = False
        self.current_volume = 50

        self.light_enabled = True
        self.previous_color = None
        self.light_is_on = False

        self.evaluando = False
        self.sensor_queue = queue.Queue()

        self.sonido_escaleras = None
        self.sonido_botones = None
        self.fondo_actual = None
        self.fondo_muteado = False

        self.mqtt_client = None
        self.running = True

        # AudioManager para audio local
        self.audio_manager = AudioManager()

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://db-maldonado-default-rtdb.firebaseio.com/'
        })

        self.TOPICO_SISTEMA = "esp32/comando/sistema"
        self.TOPICO_MODO = "escalera/control/modo_sesion"
        self.TOPICS_SENSORES = [("escalera/sensores/escalon/#", 0), ("pared/sensores/boton/#", 0)]

        self.TOPICS = [
            "rpi/audio/control",
            "rpi/audio/volume",
            "rpi/audio/status",
            "rpi/light/control",
            "rpi/light/color",
            "rpi/light/status",
            "nodered/foco/command_result",
            "nodered/foco/current_color",
            "nodered/foco/state_update",
            self.TOPICO_SISTEMA,
            self.TOPICO_MODO,
            "escalera/sensores/escalon/#",
            "pared/sensores/boton/#",
            "escalera/control/sonido_escaleras",
            "escalera/control/sonido_botones"
        ]
        self.setup_mqtt()

        self.INSTRUCCIONES = [
            ("escalon", "escalon001", "azul", "Pisa el escalon azul", "audio_files/escalon_azul.mp3"),
            ("escalon", "escalon002", "verde", "Pisa el escalon verde", "audio_files/escalon_verde.mp3"),
            ("escalon", "escalon003", "amarillo", "Pisa el escalon amarillo", "audio_files/escalon_amarillo.mp3"),
            ("escalon", "escalon004", "anaranjado", "Pisa el escalon anaranjado", "audio_files/escalon_anaranjado.mp3"),
            ("boton", "boton001", "anaranjado", "Presiona el boton anaranjado", "audio_files/boton_anaranjado.mp3"),
            ("boton", "boton002", "azul", "Presiona el boton azul", "audio_files/boton_azul.mp3"),
            ("boton", "boton003", "rosa", "Presiona el boton rosa", "audio_files/boton_rosa.mp3"),
            ("boton", "boton004", "verde", "Presiona el boton verde", "audio_files/boton_verde.mp3"),
            ("boton", "boton005", "amarillo", "Presiona el boton amarillo", "audio_files/boton_amarillo.mp3"),
            ("boton", "boton006", "morado", "Presiona el boton morado", "audio_files/boton_morado.mp3"),
        ]

        self.MAPA_COLOR_A_ID_ESCALON = {
            "azul": "escalon001",
            "verde": "escalon002",
            "amarillo": "escalon003",
            "anaranjado": "escalon004"
        }

        self.MAPA_COLOR_A_ID_BOTON = {
            "anaranjado": "boton001",
            "azul": "boton002",
            "rosa": "boton003",
            "verde": "boton004",
            "amarillo": "boton005",
            "morado": "boton006"
        }

    def obtener_id_sesion(self):
        return datetime.now().strftime('%Y-%m-%d_%H-%M')

    def timestamp_iso(self):
        return datetime.now().isoformat()

    def crear_sesion(self):
        self.sesion_id_global = self.obtener_id_sesion()
        ref = db.reference(f'sesiones/{self.sesion_id_global}')
        ref.set({
            'inicio_sesion': self.timestamp_iso(),
            'estadosesion': 'activa'
        })
        if self.modo_detectado:
            self.registrar_inicio_modo(self.modo_detectado)
            self.modo_actual = self.modo_detectado

    def registrar_inicio_modo(self, modo):
        if not self.sesion_id_global:
            return
        ref = db.reference(f'sesiones/{self.sesion_id_global}/modo{modo}')
        ref.child('inicio').set(self.timestamp_iso())

    def registrar_fin_modo(self, modo):
        if not self.sesion_id_global:
            return
        ref = db.reference(f'sesiones/{self.sesion_id_global}/modo{modo}')
        ref.child('fin').set(self.timestamp_iso())

    def finalizar_sesion(self):
        if not self.sesion_id_global:
            return
        if self.modo_actual:
            self.registrar_fin_modo(self.modo_actual)
        ref = db.reference(f'sesiones/{self.sesion_id_global}')
        ref.update({
            'fin_sesion': self.timestamp_iso(),
            'estadosesion': 'finalizada'
        })
        if self.mqtt_client:
            self.mqtt_client.publish("esp32/comando/sistema", "0")
        self.sesion_id_global = None
        self.modo_actual = None
        self.audio_manager.stop_background()

    def cambiar_modo(self, nuevo_modo):
        if not self.sesion_id_global:
            return
        if self.modo_actual and self.modo_actual != nuevo_modo:
            self.registrar_fin_modo(self.modo_actual)
        if nuevo_modo != self.modo_actual:
            self.registrar_inicio_modo(nuevo_modo)
            self.modo_actual = nuevo_modo

    def setup_mqtt(self):
        try:
            self.mqtt_client = mqtt.Client(client_id="RaspberryPi_Unified_Controller", userdata=self)
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.on_disconnect = self.on_disconnect
            self.mqtt_client.connect("localhost", 1883, 60)
        except Exception as e:
            self.mqtt_client = None

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties=None):
        pass

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            for topic in self.TOPICS:
                client.subscribe(topic)

    # ---------- Audio directo: Reproduce animal con pitch ----------
    def reproducir_audio_animal(self, animal, pitch=1.0):
        archivo = f"audio_files/{animal}.mp3"
        self.audio_manager.play_sound(archivo, pitch)

    # ---------- Musica de fondo en loop ----------
    def reproducir_fondo_modo(self, modo):
        mapa = {
            "descanso": "audio_files/modo_descanso.mp3",
            "juego": "audio_files/modo_juego.mp3",
            "evaluacion": "audio_files/modo_evaluacion.mp3"
        }
        pista = mapa.get(modo)
        if pista:
            self.fondo_actual = pista
            self.fondo_muteado = False
            self.audio_manager.play_background(pista, loop=True)

    def mute_fondo(self):
        self.audio_manager.mute_background(True)
        self.fondo_muteado = True

    def unmute_fondo(self):
        self.audio_manager.mute_background(False)
        self.fondo_muteado = False

    def mute_efectos(self):
        self.audio_manager.mute_sfx(True)

    def unmute_efectos(self):
        self.audio_manager.mute_sfx(False)

    def on_message(self, client, userdata, msg):
        topic = msg.topic

        # Configuración sonido animal
        if topic == "escalera/control/sonido_escaleras":
            self.sonido_escaleras = msg.payload.decode().strip()
            print(f"Sonido asignado a escalones: {self.sonido_escaleras}")
            self.reproducir_audio_animal(self.sonido_escaleras)
            return
        if topic == "escalera/control/sonido_botones":
            self.sonido_botones = msg.payload.decode().strip()
            print(f"Sonido asignado a botones: {self.sonido_botones}")
            self.reproducir_audio_animal(self.sonido_botones)
            return

        if (topic.startswith("escalera/sensores/escalon/") or topic.startswith("pared/sensores/boton/")):
            # Modo descanso: depuración
            if self.modo_detectado == "descanso":
                payload = msg.payload.decode(errors="ignore")
                print(f"[DEPURACION DESCANSO] TOPICO: {topic} | PAYLOAD: {payload}")
                return

            # Modo juego: registrar activaciones, reproducir sonido animal y encender led breve
            if self.modo_detectado == "juego" and self.sistema_activo and self.sesion_id_global:
                if topic.startswith("escalera/sensores/escalon/"):
                    color = topic.split("/")[-1]
                    sensor_id = self.MAPA_COLOR_A_ID_ESCALON.get(color, None)
                elif topic.startswith("pared/sensores/boton/"):
                    color = topic.split("/")[-1]
                    sensor_id = self.MAPA_COLOR_A_ID_BOTON.get(color, None)
                else:
                    sensor_id = None

                if sensor_id:
                    ruta = f"sesiones/{self.sesion_id_global}/modojuego/movimientos/{sensor_id}/"
                    ref = db.reference(ruta)
                    actual = ref.get()
                    contador = 0
                    if actual and "numero de activaciones" in actual:
                        contador = int(actual["numero de activaciones"])
                    contador += 1
                    ref.set({
                        "numero de activaciones": contador,
                        "color": color
                    })
                    print(f"[MODO JUEGO] {sensor_id} ({color}) activado. Total acumulado: {contador}")

                    # Registrar la activación con timestamp único
                    ruta_tiempos = f"sesiones/{self.sesion_id_global}/modojuego/movimientos/tiempos_movimientos"
                    ref_tiempos = db.reference(ruta_tiempos)
                    timestamp = datetime.now().isoformat().replace(":", "").replace(".", "")
                    ref_tiempos.update({timestamp: True})

                    sensor_num = int(sensor_id[-3:])
                    # Sonido animal y LED según tipo y configuración
                    if sensor_id.startswith("escalon") and self.sonido_escaleras:
                        pitch = -5.0 + 2.5 * (sensor_num - 1)
                        self.reproducir_audio_animal(self.sonido_escaleras, pitch)
                    elif sensor_id.startswith("boton") and self.sonido_botones:
                        pitch = -5.0 + 1.67 * (sensor_num - 1)
                        self.reproducir_audio_animal(self.sonido_botones, pitch)
                return

            # Si no es descanso ni juego, poner en cola (para evaluación)
            payload = msg.payload.decode(errors="ignore")
            self.sensor_queue.put((topic, payload, datetime.now().isoformat()))
            return

        if topic == self.TOPICO_SISTEMA:
            mensaje = msg.payload.decode().strip().lower()
            tiempo_actual = time.time()
            if tiempo_actual - self.ultimo_cambio_sistema < self.TIEMPO_MINIMO_ENTRE_CAMBIOS:
                return
            self.ultimo_cambio_sistema = tiempo_actual
            if mensaje in ["1", "true"]:
                if not self.sistema_activo:
                    self.sistema_activo = True
                    self.crear_sesion()
            elif mensaje in ["0", "false"]:
                if self.sistema_activo:
                    self.finalizar_sesion()
                    self.sistema_activo = False

        elif topic == self.TOPICO_MODO:
            mensaje = msg.payload.decode().strip().lower()
            modos_validos = ["descanso", "juego", "evaluacion"]
            if mensaje in modos_validos:
                self.modo_detectado = mensaje
                if self.sistema_activo and self.sesion_id_global:
                    self.cambiar_modo(mensaje)
                    if mensaje == "evaluacion" and not self.evaluando:
                        threading.Thread(target=self.modo_evaluacion).start()
                # Iniciar musica de fondo según modo
                self.reproducir_fondo_modo(self.modo_detectado)
            else:
                self.modo_detectado = None

        else:
            try:
                try:
                    message_str = msg.payload.decode('utf-8')
                except UnicodeDecodeError:
                    return
                if not message_str.strip():
                    return
                try:
                    payload = json.loads(message_str)
                except json.JSONDecodeError:
                    payload = {"value": message_str}

                # Mute selectivo: en evaluacion solo fondo
                if topic == "rpi/audio/control":
                    if self.evaluando and ("mute_fondo" in payload or ("enabled" in payload and payload["enabled"] is False)):
                        print("Muteando solo la musica de fondo (modo evaluacion)")
                        self.mute_fondo()
                        return
                    self.handle_audio_control(payload)
                elif topic == "rpi/audio/volume":
                    self.handle_volume(payload)
                elif topic == "rpi/audio/status":
                    self.send_audio_status()
                # ... resto de tu lógica (luces, etc) ...
            except Exception:
                pass

    # ---- Evaluación (idéntica a tu lógica, solo reemplazando el audio) ----
    def modo_evaluacion(self):
        self.evaluando = True
        id_sesion_eval = self.sesion_id_global
        ref_sesion = db.reference(f"sesiones/{id_sesion_eval}")
        ref_sesion.child("modoevaluacion/inicio").set(datetime.now().isoformat())

        instrucciones = random.sample(self.INSTRUCCIONES, 10)
        respuestas_correctas = 0
        respuestas_incorrectas = 0
        t_inicio = time.time()

        print("\n=== INICIO DE EVALUACION ===")
        self.audio_manager.play_sound("audio_files/evaluacion_iniciada.mp3")
        time.sleep(4)
        for orden_num, (tipo, nombre_sensor, color, texto_orden, instruccion_audio) in enumerate(instrucciones, 1):
            print("\nOrden {} de 10:".format(orden_num))
            print("  Tipo:      {}".format(tipo))
            print("  SensorID:  {}".format(nombre_sensor))
            print("  Color:     {}".format(color))
            print("  Instruccion: {}".format(texto_orden))
            print("  Tienes 30 segundos para cumplir la orden.")
            print("-"*35)

            self.audio_manager.play_sound(instruccion_audio)
            correcta = False
            timestamp_activado = None
            t0 = time.time()
            cuenta_regresiva_reproducida = False

            while True:
                tiempo_actual = time.time() - t0
                if not cuenta_regresiva_reproducida and tiempo_actual >= 20:
                    self.audio_manager.play_sound("audio_files/cuenta_regresiva.mp3")
                    cuenta_regresiva_reproducida = True
                if tiempo_actual >= 30:
                    break

                try:
                    topic, payload, tstamp = self.sensor_queue.get(timeout=0.1)
                    activado = None
                    color_del_topic = None
                    if tipo == "escalon" and topic.startswith("escalera/sensores/escalon/"):
                        color_del_topic = topic.split("/")[-1]
                        activado = self.MAPA_COLOR_A_ID_ESCALON.get(color_del_topic, None)
                    elif tipo == "boton" and topic.startswith("pared/sensores/boton/"):
                        color_del_topic = topic.split("/")[-1]
                        activado = self.MAPA_COLOR_A_ID_BOTON.get(color_del_topic, None)
                    if activado == nombre_sensor:
                        correcta = True
                        timestamp_activado = tstamp
                        print("  SENSOR CORRECTO ACTIVADO! Se marca como correcta.")
                        self.audio_manager.play_sound("audio_files/correcto.mp3")
                        respuestas_correctas += 1
                        break
                except queue.Empty:
                    continue

            if not correcta:
                respuestas_incorrectas += 1
                if not timestamp_activado:
                    timestamp_activado = datetime.now().isoformat()
                print("  No se toco el sensor correcto a tiempo. Se marca como incorrecta.")

            resumen = {
                "total_ordenes": orden_num,
                "respuestas_correctas": respuestas_correctas,
                "respuestas_incorrectas": respuestas_incorrectas
            }
            db.reference(f"sesiones/{id_sesion_eval}/resultados_evaluacion").update(resumen)

            tipo_rama = "escalones" if tipo == "escalon" else "botones"
            ruta = f"sesiones/{id_sesion_eval}/modoevaluacion/{tipo_rama}/{nombre_sensor}/"
            ref = db.reference(ruta)
            ref.set({
                "color": color,
                "correcta": correcta,
                "orden_numero": orden_num,
                "timestamp": timestamp_activado,
                "tipo_feedback": "auditiva"
            })
            time.sleep(0.5)

        t_total = round(time.time() - t_inicio, 2)
        print("\n=== FIN DE EVALUACION ===")
        print("Respuestas correctas:   {}".format(respuestas_correctas))
        print("Respuestas incorrectas: {}".format(respuestas_incorrectas))
        print("Tiempo total:           {} segundos".format(t_total))
        self.audio_manager.play_sound("audio_files/evaluacion_finalizada.mp3")

        resumen = {
            "total_ordenes": 10,
            "respuestas_correctas": respuestas_correctas,
            "respuestas_incorrectas": respuestas_incorrectas,
            "tiempo_total": t_total
        }
        db.reference(f"sesiones/{id_sesion_eval}/resultados_evaluacion").set(resumen)

        ref_sesion.child("modoevaluacion/fin").set(datetime.now().isoformat())
        db.reference("evaluacionActual/activa").set(0)
        ref_sesion.update({
            "fin_sesion": self.timestamp_iso(),
            "estadosesion": "finalizada"
        })

        self.sistema_activo = False
        self.evaluando = False

    def handle_audio_control(self, payload):
        if "enabled" in payload:
            self.audio_enabled = payload["enabled"]
            if self.audio_enabled:
                self.unmute_fondo()
                self.unmute_efectos()
            else:
                self.mute_fondo()
                self.mute_efectos()
            self.send_audio_status()

    def handle_volume(self, payload):
        if "volume" in payload:
            try:
                volume = int(payload["volume"])
                if 0 <= volume <= 100:
                    self.current_volume = volume
                    self.audio_manager.set_volume(volume)
                    self.send_audio_status()
            except (ValueError, TypeError):
                pass

    def get_volume(self):
        try:
            result = subprocess.run(['amixer', 'sget', 'Master'],
                                   capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                import re
                match = re.search(r'\[(\d+)%\]', result.stdout)
                if match:
                    return int(match.group(1))
        except Exception:
            pass
        return self.current_volume

    def send_audio_status(self):
        if self.mqtt_client is None:
            return
        status = {
            "enabled": self.audio_enabled,
            "volume": self.current_volume,
            "system_volume": self.get_volume(),
            "timestamp": time.time()
        }
        try:
            self.mqtt_client.publish("rpi/audio/status/update", json.dumps(status))
        except Exception:
            pass

    def handle_light_control(self, payload):
        if "enabled" in payload:
            self.light_enabled = payload["enabled"]
            if self.light_enabled:
                self.light_turn_on()
            else:
                self.light_turn_off()
            self.send_light_status()

    def handle_light_color(self, payload):
        if "color" in payload:
            color = payload["color"]
            if isinstance(color, dict) and "r" in color and "g" in color and "b" in color:
                self.set_temp_light_color(color["r"], color["g"], color["b"])

    def handle_current_color_response(self, payload):
        if "color" in payload:
            self.previous_color = payload["color"]

    def handle_state_update(self, payload):
        if "is_on" in payload:
            self.light_is_on = payload["is_on"]

    def send_light_command(self, action, **kwargs):
        if self.mqtt_client is None:
            return
        command = {
            "action": action,
            "id": str(int(time.time() * 1000)),
            **kwargs
        }
        try:
            self.mqtt_client.publish("python/foco/command", json.dumps(command))
            time.sleep(0.1)
        except Exception:
            pass

    def set_temp_light_color(self, r, g, b):
        if not self.light_is_on:
            return
        try:
            r, g, b = int(r), int(g), int(b)
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.send_light_command("get_color")
                time.sleep(0.1)
                self.send_light_command("temp_color", color={"r": r, "g": g, "b": b})
                timer = threading.Timer(2.0, self.restore_light_color)
                timer.start()
        except (ValueError, TypeError):
            pass

    def restore_light_color(self):
        if self.previous_color:
            self.send_light_command("set_color", color=self.previous_color)
        else:
            self.send_light_command("restore_color")

    def light_turn_on(self):
        self.send_light_command("turn_on")

    def light_turn_off(self):
        self.send_light_command("turn_off")

    def send_light_status(self):
        if self.mqtt_client is None:
            return
        status = {
            "enabled": self.light_enabled,
            "is_on": self.light_is_on,
            "timestamp": time.time()
        }
        try:
            self.mqtt_client.publish("rpi/light/status/update", json.dumps(status))
        except Exception:
            pass

    def stop(self, signum=None, frame=None):
        self.running = False
        if self.mqtt_client:
            try:
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            except Exception:
                pass
        if self.sistema_activo:
            self.finalizar_sesion()
        self.audio_manager.quit()
        sys.exit(0)

    def run(self):
        if self.mqtt_client is None:
            print("No se pudo conectar al broker MQTT.")
            return
        try:
            self.mqtt_client.loop_start()
            time.sleep(1)
            self.send_audio_status()
            self.send_light_status()
            self.send_light_command("get_state")
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        except Exception:
            pass

if __name__ == "__main__":
    controller = UnifiedController()
    controller.run()