import socket
import sys
from time import sleep

# VARIABLES GLOBALES
HOST = '127.0.0.1'              # Host del servidor (localhost)
PORT = 4628                     # Puerto por defecto
BUF_S = 1024                    # Tamaño del buffer
ENC = "utf-8"                   # Encoding por defecto


def cod_msj(*cad, sep=' ', enc=ENC):
    """Convierte cadenas a `bytes` codificados `utf-8`."""
    # Combina todas las cadenas en la variable `cad`,
    # Que es una lista de n cadenas, en una sola cadena,
    # Separadas c/u por un separador.
    cadena_total = sep.join(cad)
    return bytes(cadena_total, encoding=enc)


if __name__ == '__main__':
    # Crea una variable `server`, de la clase `socket` con dos
    # Parámetros especiales.
    # Esta variable es el servidor del Chat.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Intenta alojar el servidor en `HOST:PORT`
    server.bind((HOST, PORT))

    # Activa el servidor para que "escuche" otras conexiones
    server.listen()

    try:
        while True:
            # Espera a que algún cliente se conecte.
            # Cuando lo haga, almacena el socket en `client`
            # Y su dirección `(HOST, PORT)` en `direc`.
            client, direc = server.accept()
            cad_direc = f'{direc[0]}:{direc[1]}'
            print(f"Cliente conectado: {cad_direc}")

            client.send(cod_msj(f"[{HOST}:{PORT}]: Connectado."))
            imsg = client.recv(BUF_S).decode(ENC)
            print(f'[{cad_direc}]: {imsg}')
            sleep(16)
            client.send(cod_msj(f"[{HOST}:{PORT}]: Desconectado por timeout."))
            client.close()

    except KeyboardInterrupt:
        # Si el programa es abortado por `^C` (CTRL + c),
        # En lugar de abortar por completo el programa,
        # Hacer lo siguiente
        print("Abortando...")
        # client.close()

    finally:
        server.close()
        sys.exit(0)
