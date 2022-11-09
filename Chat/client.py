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
    # Primero Crea El Socket Del Cliente,
    # Un objeto de tipo `socket.socket()`
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta con el servidor dados
        # `HOST` y `PORT`
        cli_sock.connect((HOST, PORT))

        # Espera un mensaje del servidor,
        # De ahí decodificar e imprimir.
        msg1 = cli_sock.recv(BUF_S).decode(ENC)
        print(msg1)

        # Codifica y manda `omsg` al servidor,
        # Que debería estar esperando por algún mensaje.
        omsg = "¡Hola! ¡Soy un nuevo cliente!"
        cli_sock.send(cod_msj(omsg))

        # Espera un mensaje de despedida del servidor,
        # De ahí decodificar e imprimir.
        msg2 = cli_sock.recv(BUF_S).decode(ENC)
        print(msg2)

    except ConnectionError:
        # No hay ningún servidor en la ruta indicada.
        print("ERROR: No hay ningún servidor activo",
              f'en {HOST}:{PORT}')

    except ConnectionAbortedError:
        # Se cerró el servidor.
        print("ERROR: Se perdió la conexión con el servidor.")

    except KeyboardInterrupt:
        # Si este programa se cancela usando `^C`
        # (`CTRL + c`)
        print("Abortando.")

    # TODO: Decidir si incluir cualquier otra excepción
    #       genérica.

    # except Exception:
    #    # Cualquier otro error.
    #    print('Algo salió mal.')

    finally:
        # Haya o no haya error, cerrar cliente.
        cli_sock.close()

    sys.exit(0)
