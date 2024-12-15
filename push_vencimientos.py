import pymysql
import tkinter as tk
from tkinter import messagebox
from plyer import notification
from datetime import datetime, timedelta

# Configuración de la base de datos
db_config = {
    'host': '127.0.0.1', # Dirección del servidor de la base de datos
    'user': 'root',       # Tu usuario de MySQL
    'password': '1234',       # Tu contraseña de MySQL
    'database': 'prueba_crud',  # Nombre de la base de datos
}

def conectar_bd():
    """Conectar a la base de datos MySQL."""
    try:
        conexion = pymysql.connect(**db_config)
        print("conexion ok")
        return conexion
    except pymysql.MySQLError as e:
        print(f"Error de conexión: {e}")
        return None

def verificar_eventos():
    """Verificar los eventos próximos y mostrar notificaciones."""
    conexion = conectar_bd()
    if conexion:
        # Obtener la fecha actual
        fecha_actual = datetime.now().date()
        # Consultar los eventos que estén dentro de 7 días
        fecha_limite = fecha_actual + timedelta(days=7)
        
        with conexion.cursor() as cursor:
            query = "SELECT nombre_evento, fecha_evento FROM eventos WHERE fecha_evento BETWEEN %s AND %s"
            cursor.execute(query, (fecha_actual, fecha_limite))
            eventos_proximos = cursor.fetchall()
            
            if eventos_proximos:
                for evento in eventos_proximos:
                    nombre_evento, fecha_evento = evento
                    # fecha_evento = fecha_evento.date()
                    # Notificar en la interfaz gráfica
                    mostrar_notificacion(nombre_evento, fecha_evento)
                    # Notificación del sistema
                    notificar_sistema(nombre_evento, fecha_evento)
            else:
                print("No hay eventos próximos.")
        conexion.close()

def mostrar_notificacion(nombre_evento, fecha_evento):
    """Mostrar una notificación en la interfaz gráfica."""
    messagebox.showinfo(
        "Evento próximo",
        f"El evento '{nombre_evento}' será el {fecha_evento}. ¡No lo olvides!"
    )

def notificar_sistema(nombre_evento, fecha_evento):
    """Mostrar una notificación del sistema."""
    notification.notify(
        title="Evento próximo",
        message=f"El evento '{nombre_evento}' será el {fecha_evento}. ¡No lo olvides!",
        timeout=10  # La notificación durará 10 segundos
    )

def iniciar_ventana():
    """Iniciar la ventana principal de Tkinter."""
    ventana = tk.Tk()
    ventana.title("Notificador de Eventos")
    ventana.geometry("300x200")
    
    label = tk.Label(ventana, text="Sistema de notificaciones de eventos")
    label.pack(pady=20)

    # Botón para verificar eventos
    btn_verificar = tk.Button(ventana, text="Verificar eventos", command=verificar_eventos)
    btn_verificar.pack(pady=10)

    ventana.mainloop()

# EN CASO DE QUERER VERIFICAR AUTOMATICAMENTE EN UNA MINUTO

# def iniciar_ventana():
#     """Iniciar la ventana principal de Tkinter."""
#     ventana = tk.Tk()
#     ventana.title("Notificador de Eventos")
#     ventana.geometry("300x200")
    
#     label = tk.Label(ventana, text="Sistema de notificaciones de eventos")
#     label.pack(pady=20)

#     # Botón para verificar eventos manualmente
#     btn_verificar = tk.Button(ventana, text="Verificar eventos", command=verificar_eventos)
#     btn_verificar.pack(pady=10)

#     # Función para verificar eventos cada 60 segundos (60000 ms)
#     def verificar_periodicamente():
#         verificar_eventos()
#         ventana.after(60000, verificar_periodicamente)  # Verificar nuevamente después de 1 minuto

#     # Iniciar verificación periódica
#     verificar_periodicamente()

#     ventana.mainloop()
    
    
    
# Ejemplo de uso
if __name__ == "__main__":
    # Iniciar la ventana
    iniciar_ventana()

    # Verificar eventos al iniciar el programa (puedes agregar esta función a un cronómetro)
    verificar_eventos()
