import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/sesion"

# Cambia este ID por uno válido en tu base de datos
test_id_nino = 1

# --- Probar inicio de sesión ---
def test_iniciar_sesion():
    payload = {
        "id_nino": test_id_nino,
        "tipo_evaluacion": "diagnóstica",
        "observaciones_inicio": "Prueba automática de inicio de sesión"
    }
    print("\n[TEST] Enviando solicitud para INICIAR sesión...")
    resp = requests.post(f"{BASE_URL}/iniciar", json=payload)
    print("Status:", resp.status_code)
    try:
        print("Respuesta:", resp.json())
    except Exception:
        print("Respuesta:", resp.text)

# --- Probar finalización de sesión ---
def test_finalizar_sesion():
    payload = {
        "id_nino": test_id_nino,
        "observaciones_final": "Prueba automática de cierre de sesión"
    }
    print("\n[TEST] Enviando solicitud para FINALIZAR sesión...")
    resp = requests.post(f"{BASE_URL}/finalizar", json=payload)
    print("Status:", resp.status_code)
    try:
        print("Respuesta:", resp.json())
    except Exception:
        print("Respuesta:", resp.text)

if __name__ == "__main__":
    test_iniciar_sesion()
    test_finalizar_sesion()
