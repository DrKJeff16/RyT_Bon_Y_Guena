import socket
import time

# VARIABLES GLOBALES
HOST = '127.0.0.1'              # Host del servidor
PORT = 4628                     # Puerto por defecto
BUF_S = 1024                    # Tamaño del buffer


# Crea una variable `sock`, de la clase `socket` con dos
# Parámetros especiales
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Aloja el servidor en el HOST:PORT
sock.bind((HOST, PORT))

# Activa el servidor para que "escuche" otras conexiones
sock.listen()

try:
    while True:
        clientsocket, address = sock.accept()
        print("Connection is stablished", address)
        clientsocket.send(bytes("Server: You are connected", encoding='utf-8'))
        msg = clientsocket.recv(1024)
        print(msg.decode("utf-8"))
        time.sleep(120)
        clientsocket.send(bytes("bye"))
        clientsocket.close()
except KeyboardInterrupt:
    print ("Finishing . . .")
sock.close()
