from Model.CompaniaModel import CompaniaModel
from Views.Companias.companias_view import CompaniasView


class CompaniaController:
    def __init__(self, root, db_connection):
        self.compania_model = CompaniaModel(db_connection)
        self.companias_view = CompaniasView(root, self.compania_model)

    def load_view(self):
        
       self.companias_view.load_Companias()  # Cargar las compañias en la vista al iniciar
       
       