import firebase_admin
from firebase_admin import credentials, db

# Ruta absoluta al archivo JSON
import os

# Get the directory of the current file (__init__.py), which is 'my-app'
current_dir = os.path.abspath(os.path.dirname(__file__))

# Go up one level from 'my-app' to the 'GRUPO1' directory
project_root_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Now join the project root with the key_firebase.json filename
firebase_path = os.path.join(project_root_dir, 'key_firebase.json')

# Inicializar Firebase solo si no está ya inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://db-maldonado-default-rtdb.firebaseio.com/'
    })