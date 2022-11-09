import socket
import sys

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
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sock.connect((HOST, PORT))

        msg1 = cli_sock.recv(BUF_S).decode(ENC)
        print(msg1)
        cli_sock.send(cod_msj("[CLIENTE]: ¡Hola! Soy un nuevo cliente!"))
        msg2 = cli_sock.recv(BUF_S).decode(ENC)
        print(msg2)

    except ConnectionError:
        # No hay ningún servidor en la ruta indicada
        print("ERROR: No hay ningún servidor activo",
              f'en {HOST}:{PORT}')

    except ConnectionAbortedError:
        # TODO: Se cerró el servidor(?)
        print("ERROR: Se perdió la conexión con el servidor.")

    except KeyboardInterrupt:
        # Si este programa se cancela usando
        # `CTRL + c`
        print("Abortando.")

    except Exception:
        # Cualquier otro error.
        print('Algo salió mal.')

    finally:
        cli_sock.close()

    sys.exit(0)
