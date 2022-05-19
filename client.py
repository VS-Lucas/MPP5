import socket

class Client:
    def __init__(self, _ip, _port):
        self.con = (_ip, _port)
        self.buildSocketTCP()
        self.buildSocketUDP()

    def buildSocketTCP(self):
        # Criando o canal de comunicação TCP entre client -> servidor
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect(self.con)
    def buildSocketUDP(self):
        # Criando o canal de comunicação TCP entre client -> servidor
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect(self.con)

client = Client('168.196.41.100', 55555)

