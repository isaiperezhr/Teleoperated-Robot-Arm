import socket
from dotenv import load_dotenv
import os


# Cargamos las variables de entorno
load_dotenv()

# Configuración del servidor
HOST = os.getenv("SERVER_IP")  # Dirección IP local
PORT = int(os.getenv("SERVER_PORT"))        # Puerto del servidor

# Crear un socket para el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Servidor en espera de conexiones...")

    while True:  # Bucle principal para mantener el servidor abierto
        conn, addr = server_socket.accept()
        print(f"Conectado por {addr}")

        with conn:  # Manejar la conexión con el cliente
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Cliente {addr} desconectado")
                    break  # Terminar el bucle para este cliente, pero mantener el servidor activo
                print(f"Valores recibidos de {addr}: {data.decode()}")
