import socket
import os

class Client:
    def __init__(self, _ip, _port):
        self.con = (_ip, _port)
        self.buildSocketUDP()
        # self.buildSocketUDP()

    def buildSocketUDP(self):
        # Criando o canal de comunicação TCP entre client -> servidor
        sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckt.connect(self.con)

    def sendfile(self):
        pathsize = os.path.getsize()
        with open("path-50Gb.pdf", 'rb') as file:
            
            pass
        pass
    # def buildSocketUDP(self):
    #     # Criando o canal de comunicação UDP entre client -> servidor
    #     sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sckt.connect(self.con)

client = Client('179.152.253.19', 55555, 40000)

