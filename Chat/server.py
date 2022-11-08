import socket
import time

# VARIABLES GLOBALES
HOST = '127.0.0.1'              # Host del servidor (localhost)
PORT = 4628                     # Puerto por defecto
BUF_S = 1024                    # Tamaño del buffer
ENC = "utf-8"                   # Encoding por defecto


def cod_msj(*cad):
    """Convierte cadenas a `bytes` codificados."""
    # Combina todas las cadenas en
    cadena_total = ' '.join(cad)

    return bytes(cadena_total, encoding=ENC)


# Crea una variable `server`, de la clase `socket` con dos
# Parámetros especiales.
# Esta variable es el servidor del Chat.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Aloja el servidor en el HOST:PORT
server.bind((HOST, PORT))

# Activa el servidor para que "escuche" otras conexiones
server.listen()

try:
    while True:
        clientsocket, address = server.accept()
        print("Connection is stablished", address)
        clientsocket.send(bytes("Server: You are connected", encoding=ENC))
        msg = clientsocket.recv(BUF_S)
        print(msg.decode(ENC))
        time.sleep(120)
        clientsocket.send(bytes("bye"))
        clientsocket.close()
except KeyboardInterrupt:
    print("Finishing . . .")

server.close()
