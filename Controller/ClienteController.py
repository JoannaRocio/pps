from Model.ClienteModel import ClienteModel
from Views.Clientes.clientes_view import ClientesView


class ClienteController:
    def __init__(self, root, db_connection):
        self.cliente_model = ClienteModel(db_connection)
        self.clientes_view = ClientesView(root, self.cliente_model)

    def mostrar_vista_clientes(self):
        # Aquí puedes realizar cualquier configuración adicional necesaria
       self.clientes_view.load_clients()  # Cargar los clientes en la vista al iniciar
