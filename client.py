import socket
import os

class Client:
    def __init__(self, _ip: str, _port: int, _path: str, _buffer: int) -> None:
        self.con = (_ip, _port)
        self.path = _path
        self.BUFFER = _buffer
        
        self.buildSocketUDP()
        self.sendfile()
        self.recvfile()

    def buildSocketUDP(self) -> None:
        # Criando o canal de comunicação TCP entre client -> servidor
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.connect(self.con)

    def sendfile(self) -> None:
        pathsize = os.path.getsize(self.path)
        print(pathsize)
        self.sckt.sendall(bytes(f'Enviando arquivo: {self.path} | {pathsize} bytes', 'utf-8'))

        with open(self.path, 'rb') as file:
            byte_data = file.read(self.BUFFER)
            while byte_data:
                self.sckt.send(byte_data)
                byte_data = file.read(self.BUFFER)
 
        print('Arquivo enviado com sucesso!')
    
    def recvfile(self) -> None:
        self.sckt.recv(1024)
        with open(self.path, 'wb') as file:
            byte_data = self.sckt.recv(self.BUFFER)
            pathsize -= self.BUFFER
            while pathsize > 0:
                file.write(byte_data)
                byte_data = self.sckt.recv(self.BUFFER)
                pathsize -= self.BUFFER
        print('Arquivo recebido')
        file.close()
    
    def send_message(self):
        pass
    
    def recv(self):
        pass

client = Client('45.239.196.96', 55555, "path-54MB.pdf", 50000)

