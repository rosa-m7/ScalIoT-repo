import mysql.connector

def connectionBD():
    print("ENTRO A LA CONEXION")
    try:
        connection = mysql.connector.connect(
            host="35.223.160.190",
            port=3306,
            user="root",
            passwd="Passw0rd.1",
            database="Proyecto_Escalera_Pared",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            print("Conexión exitosa a la BD En la Nube")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
