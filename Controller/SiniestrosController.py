"""class SiniestrosController:
    def __init__(self, siniestros_model, siniestros_view):
        self.siniestros_model = siniestros_model  # El modelo que maneja los datos
        self.siniestros_view = siniestros_view  # La vista que mostrará los datos

    def ver_siniestros(self):
        # Obtienes los siniestros desde el modelo
        siniestros = self.siniestros_model.mostrar_siniestros()
        
        # Ordenas los siniestros (puedes modificar la lógica si es necesario)
        siniestros_ordenados = sorted(siniestros, key=lambda x: (x[1], x[2]))
        
        # Pasas los datos ordenados a la vista para que los muestre
        self.siniestros_view.mostrar_siniestros(siniestros_ordenados)
"""