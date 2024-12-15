class LoginController:
    def __init__(self, modelo_usuario, vista_usuario, on_login_success):
        self.modelo_usuario = modelo_usuario
        self.vista_usuario = vista_usuario
        self.on_login_success = on_login_success
        
    def set_view(self, vista_usuario):
        self.vista_usuario = vista_usuario

    def verificar_credenciales(self, usuario, contrasena):
        # Verificar si hay usuarios en la base de datos
        if self.modelo_usuario.obtener_cantidad_usuarios() == 0:
            # Si no hay usuarios, mostrar la vista de registro
            self.vista_usuario.mostrar_vista_registro()
            return False
        
        # Verificar las credenciales del usuario
        usuario_encontrado = self.modelo_usuario.verificar_credenciales(usuario, contrasena)
        
        if usuario_encontrado:
            # Si las credenciales son correctas, ejecutar la acción de éxito
            self.on_login_success(usuario_encontrado[0])  # Llamar a la función de éxito (por ejemplo, cambiar de vista)
            return True
        
        # Si las credenciales no son correctas, retornar False
        return False

    def cambiar_contrasena(self, id, nueva_contrasena):
        # Cambiar la contraseña del usuario
        self.modelo_usuario.actualizar_contrasena(id, nueva_contrasena)

    def registrar_usuario(self, usuario, contrasena):
        # Registrar un nuevo usuario
        self.modelo_usuario.registrar_usuario(usuario, contrasena)

    def on_login_success(usuario):
    # Aquí puedes cambiar la vista o realizar otras acciones al loguearse correctamente
        print(f"Usuario {usuario} ha iniciado sesión correctamente.")
    # Llamar a otra vista o cambiar la pantalla, etc.
