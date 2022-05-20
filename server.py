import socket
import os

class Server:
    def __init__(self, _ip: str, _port: int, _buffer: int) -> None:
        self.con = (_ip, _port)
        self.BUFFER = _buffer
        self.buildSocketTCP()
        self.recvfile()
        self.sendfile()
        

    def buildSocketTCP(self):
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.bind(self.con)
        sckt.listen(2)
        self.client1, self.addr1 = sckt.accept()
    
        print('Primeiro usuário conectado')

    def sendfile(self) -> None:
        pathsize = os.path.getsize(self.file)
        self.client1.sendall(bytes(f'Enviando arquivo: {self.file} | {pathsize} bytes', 'utf-8'))

        with open(self.file, 'rb') as file:
            byte_data = file.read(self.BUFFER)
            while byte_data:
                self.client1.send(byte_data)
                byte_data = file.read(self.BUFFER)
        print('Arquivo enviado com sucesso!')

    def recvfile(self) -> None:
        self.msg = self.client1.recvfrom(1024)
        self.size = int(self.msg[0].split()[4].decode())
        self.file = self.msg[0].split()[2].decode()

        with open(self.file, 'wb') as file:
            byte_data = self.client1.recv(self.BUFFER)
            self.size -= self.BUFFER
            try:
                while self.size > 0:
                    file.write(byte_data)
                    byte_data = self.client1.recv(self.BUFFER)
                    self.size -= self.BUFFER
            except:
                print('error no except')
        print('Arquivo recebido')
        file.close()

    def send(self) -> None:
        pass

    def recv(self) -> None:
        pass
        
client = Server('192.168.0.84', 55555, 100000)
