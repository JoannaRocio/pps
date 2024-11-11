class VencimientosController:
    def __init__(self, vencimiento_model, vencimientos_view):
        self.vencimiento_model = vencimiento_model  # El modelo que maneja los datos
        self.vencimientos_view = vencimientos_view  # La vista que mostrará los datos

    def ver_vencimientos(self):
        # Obtienes los vencimientos desde el modelo
        vencimientos = self.vencimiento_model.mostrar_vencimientos()
        
        # Ordenas los vencimientos (puedes modificar la lógica si es necesario)
        vencimientos_ordenados = sorted(vencimientos, key=lambda x: (x[1], x[2]))
        
        # Pasas los datos ordenados a la vista para que los muestre
        self.vencimientos_view.mostrar_vencimientos(vencimientos_ordenados)
