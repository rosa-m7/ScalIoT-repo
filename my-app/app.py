from flask import Flask
import pytz
from datetime import datetime
import os

app = Flask(__name__)
application = app
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

# ===== CONFIGURACIÓN GLOBAL DE ZONA HORARIA =====
# Configurar zona horaria de Ecuador
ECUADOR_TZ = pytz.timezone('America/Guayaquil')

# Función global para obtener hora de Ecuador
def get_ecuador_time():
    """Retorna la hora actual en zona horaria de Ecuador"""
    return datetime.now(ECUADOR_TZ)

def format_ecuador_time(dt=None):
    """Formatea la fecha/hora para bases de datos"""
    if dt is None:
        dt = get_ecuador_time()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Hacer las funciones disponibles globalmente en la app
app.get_ecuador_time = get_ecuador_time
app.format_ecuador_time = format_ecuador_time

# También puedes configurar la zona horaria del sistema (opcional)
os.environ['TZ'] = 'America/Guayaquil'
# ===== FIN CONFIGURACIÓN ZONA HORARIA =====

from routers.router_analitica import bp_analitica
print('*** Registrando blueprint bp_analitica', flush=True)
app.register_blueprint(bp_analitica)