class UsuarioModel:
    def verificar_credenciales(self, username, password):
        # Aquí puedes tener tu lógica de autenticación real
        if username == "1" and password == "1":  # Ejemplo estático
            return True
        return False
