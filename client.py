import tkinter as tk
import socket

# Variables globales para el socket y el estado de conexión
client_socket = None
conectado = False

# Función para enviar los valores de los sliders al servidor
def enviar_valores():
    if conectado:
        valores = ','.join([str(slider.get()) for slider in sliders])
        client_socket.sendall(valores.encode())

# Función para conectar o desconectar del servidor
def conectar_desconectar():
    global client_socket, conectado

    if not conectado:  # Si no está conectado, intenta conectar
        ip = entry_ip.get()
        puerto = int(entry_puerto.get())

        try:
            # Crear el socket del cliente
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, puerto))
            status_label.config(text="Conectado", fg="green")
            
            # Habilitar los sliders
            for slider in sliders:
                slider.config(state="normal")
            
            # Cambiar estado a conectado
            conectado = True
            boton_conectar.config(text="Desconectar")  # Cambiar texto del botón

        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="red")

    else:  # Si ya está conectado, desconecta
        try:
            client_socket.close()  # Cerrar el socket
        except Exception as e:
            status_label.config(text=f"Error al desconectar: {str(e)}", fg="red")

        # Deshabilitar los sliders
        for slider in sliders:
            slider.config(state="disabled")
        
        status_label.config(text="Desconectado", fg="red")
        conectado = False
        boton_conectar.config(text="Conectar")  # Cambiar texto del botón

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Control de Servomotores")
root.geometry("400x500")
root.configure(bg="black")

# Título de la interfaz
titulo_label = tk.Label(root, text="Robot Arm Control", bg="black", fg="white", font=("Arial", 16, "bold"))
titulo_label.pack(pady=10)

# Sección de entrada para IP y Puerto
frame_conexion = tk.Frame(root, bg="black")
frame_conexion.pack(pady=10)

label_ip = tk.Label(frame_conexion, text="IP del Servidor:", bg="black", fg="white", font=("Arial", 10))
label_ip.pack(pady=5)
entry_ip = tk.Entry(frame_conexion)
entry_ip.pack()

label_puerto = tk.Label(frame_conexion, text="Puerto:", bg="black", fg="white", font=("Arial", 10))
label_puerto.pack(pady=5)
entry_puerto = tk.Entry(frame_conexion)
entry_puerto.pack()

# Botón para conectar/desconectar al servidor
boton_conectar = tk.Button(frame_conexion, text="Conectar", command=conectar_desconectar, bg="gray", fg="white")
boton_conectar.pack(pady=10)

# Etiqueta de estado de conexión
status_label = tk.Label(frame_conexion, text="Desconectado", bg="black", fg="red", font=("Arial", 10))
status_label.pack()

# Crear un marco para organizar los sliders
frame_sliders = tk.Frame(root, bg="black")
frame_sliders.pack(pady=20, padx=20)

# Crear los sliders
sliders = []
for i in range(6):
    slider_frame = tk.Frame(frame_sliders, bg="black")
    slider_frame.pack(pady=5)

    label = tk.Label(slider_frame, text=f"Servo {i+1}", bg="black", fg="white", font=("Arial", 10))
    label.pack(side="left", padx=5)

    slider = tk.Scale(slider_frame, from_=0, to=180, orient=tk.HORIZONTAL, length=250, 
                      troughcolor="gray", bg="black", fg="white", highlightbackground="white")
    slider.pack(side="right")
    slider.config(command=lambda x: enviar_valores(), state="disabled")  # Inicialmente deshabilitado
    sliders.append(slider)

# Iniciar la interfaz
root.mainloop()

# Cerrar el socket si está conectado al cerrar la ventana
if client_socket:
    client_socket.close()
    