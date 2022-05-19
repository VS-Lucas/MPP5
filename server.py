import socket

class Server:
    def __init__(self, _ip: str, _port: int):
        self.con = (_ip, _port)
        self.buildSocketTCP()

    def buildSocketTCP(self):
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.bind(self.con)
        sckt.listen(2)
        self.client1, self.addr1 = sckt.accept()
        print('Primeiro usuário conectado')
        self.client2, self.addr2 = sckt.accept()
        print('Segundo usuário conectado')

    def send(self):
        pass

    def recv(self):
        pass
        
client = Server('192.168.1.7', 55555)