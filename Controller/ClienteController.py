from ClienteModel import ClienteModel
from ClienteView import ClienteView


class ClienteController:
    def __init__(self, root, db_connection):
        self.cliente_model = ClienteModel(db_connection)
        self.cliente_view = ClienteView(root, self.cliente_model)

    def load_view(self):
        # Aquí puedes realizar cualquier configuración adicional necesaria
       self.cliente_view.load_clients()  # Cargar los clientes en la vista al iniciar
