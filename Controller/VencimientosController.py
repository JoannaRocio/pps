

class VencimientosController:
    def __init__(self, vencimiento_model, view):
        self.model = vencimiento_model
        self.view = view

    def ver_vencimientos(self):
        vencimientos = self.model.mostrar_vencimientos() or []
        if not vencimientos:  # Si no hay vencimientos
            from tkinter import messagebox
            messagebox.showinfo("Sin Vencimientos", "No hay vencimientos registrados.")
        self.view.actualizar_vencimientos(vencimientos)

    def buscar_cliente(self, search_term):
        vencimientos = self.model.mostrar_vencimientos()
        resultados = [v for v in vencimientos if search_term.lower() in v[0].lower() or search_term.lower() in v[1].lower() or search_term.lower() in v[2].lower()]
        self.view.actualizar_vencimientos(resultados)

    def mostrar_notificaciones(self):
        vencimientos = self.model.mostrar_vencimientos()
        proximos_vencimientos = [v for v in vencimientos if self.esta_por_vencer(v)]
        self.view.mostrar_notificaciones(proximos_vencimientos)

    def esta_por_vencer(self, vencimiento):
        from datetime import datetime, timedelta
        fecha_licencia = datetime.strptime(vencimiento[3], "%Y-%m-%d")
        fecha_poliza = datetime.strptime(vencimiento[4], "%Y-%m-%d")
        return fecha_licencia <= datetime.now() + timedelta(days=15) or fecha_poliza <= datetime.now() + timedelta(days=15)

    def abrir_sitio_web(self, sitio_web):
        import webbrowser
        webbrowser.open(sitio_web)
