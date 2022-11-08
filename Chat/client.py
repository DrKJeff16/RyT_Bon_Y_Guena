import socket

HOST = '127.0.0.1'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 4000))

msg = sock.recv(1024)
print(msg.decode("utf-8"))
sock.send(bytes("Client: Thank you, I'm your client number 1", encoding='utf-8'))
#msg1 = sock.recv(1024)
#print(msg1.decode("utf-8"))

sock.close()
