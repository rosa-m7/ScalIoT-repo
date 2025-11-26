import mysql.connector

def connectionBD():
    print("ENTRO A LA CONEXION")
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MARIADB_HOST", "192.168.1.100"),  # IP de tu RPi
            port=int(os.getenv("MARIADB_PORT", 3306)),
            user=os.getenv("MARIADB_USER", "grupo1_remote"),
            passwd=os.getenv("MARIADB_PASSWORD", "Passw0rd.1"),
            database=os.getenv("MARIADB_DATABASE", "grupo1"),  # Nombre correcto de tu BD
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True,
            autocommit=True,
            connection_timeout=10  # Timeout de 10 segundos
        )
        if connection.is_connected():
            print("Conexión exitosa a la BD MariaDB")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
