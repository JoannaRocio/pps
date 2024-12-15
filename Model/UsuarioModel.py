import mysql.connector
import bcrypt

class UsuarioModelo:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = self.db_connection.connection.cursor()
        
    def obtener_cantidad_usuarios(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        return self.cursor.fetchone()[0]  

    def obtener_usuario_count(self):
        # Verificar cuántos usuarios hay en la base de datos
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        return self.cursor.fetchone()[0]

    def verificar_credenciales(self, usuario, contrasena):
    # Realiza la consulta para obtener el id y la contraseña
        self.cursor.execute("SELECT id, contrasena FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_encontrado = self.cursor.fetchone()

        if usuario_encontrado:
        # Compara la contraseña proporcionada con la almacenada en la base de datos
            if bcrypt.checkpw(contrasena.encode('utf-8'), usuario_encontrado[1].encode('utf-8')):
                return usuario_encontrado  # Devuelve el id y la contraseña (o más datos si los necesitas)
    
        return None  # Si no se encuentra el usuario o las contraseñas no coinciden

    def actualizar_contrasena(self, id_usuario, nueva_contrasena):
        hashed_contrasena = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("UPDATE usuarios SET contrasena = %s, primer_ingreso = FALSE WHERE id = %s", 
                            (hashed_contrasena, id_usuario))
        self.db_connection.connection.commit()

    def verificar_primer_ingreso(self, id_usuario):
        self.cursor.execute("SELECT primer_ingreso FROM usuarios WHERE id = %s", (id_usuario,))
        resultado = self.cursor.fetchone()
        return resultado[0]

    def registrar_usuario(self, usuario, contrasena):
        # Verificar si ya existe un usuario con ese nombre
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", (usuario,))
        if self.cursor.fetchone()[0] > 0:
            raise ValueError("El usuario ya está registrado.")
        
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("INSERT INTO usuarios (usuario, contrasena, primer_ingreso) VALUES (%s, %s, %s)", 
                            (usuario, hashed_contrasena, True))
        self.db_connection.connection.commit()
