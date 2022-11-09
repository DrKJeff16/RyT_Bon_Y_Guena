import socket

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


cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((HOST, PORT))

msg = sock.recv(BUF_S).decode(ENC)
print(msg)
cli_sock.send(cod_msj("Client: Thank you, I'm your client number 1"))
msg1 = cli_sock.recv(BUF_S).decode(ENC)
print(msg1)

cli_sock.close()
