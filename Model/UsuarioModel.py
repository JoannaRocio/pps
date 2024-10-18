class UsuarioModel:
    def verificar_credenciales(self, username, password):
        # Aquí puedes tener tu lógica de autenticación real
        if username == "admin" and password == "password":  # Ejemplo estático
            return True
        return False
