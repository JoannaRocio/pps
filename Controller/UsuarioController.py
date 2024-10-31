from Views.UsuarioView import UsuarioView  # Asegúrate de que la ruta sea correcta
from Model.UsuarioModel import UsuarioModel  # Asegúrate de que la ruta sea correcta

class UsuarioController:
    def __init__(self, root):
        self.usuario_model = UsuarioModel()
        self.usuario_view = UsuarioView(root, self.usuario_model, self.on_login_success)

    def on_login_success(self):
        # Aquí es donde inicias el dashboard o la vista principal
        print("Inicio de sesión exitoso, cargando el dashboard...")
        # Llama a la función para cargar el dashboard
        self.load_dashboard()

    def load_dashboard(self):
        # Lógica para inicializar y mostrar el dashboard
        from Dashboard import Dashboard  # Ajusta según tu estructura de carpetas
        dashboard = Dashboard()
        dashboard.run()
