import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 4000))
sock.listen(1)

try:
    while True:
        clientsocket, address = sock.accept()
        print("Connection is stablished", address)
        clientsocket.send(bytes("Server: You are connected", encoding='utf-8'))
        msg = clientsocket.recv(1024)
        print(msg.decode("utf-8"))
        #time.sleep(120)
        #clientsocket.send(bytes("bye"))
        clientsocket.close()
except KeyboardInterrupt:
    print ("Finishing . . .")
    
sock.close()
