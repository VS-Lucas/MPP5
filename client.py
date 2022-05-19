import socket



class Client:
    def __init__(self, _ip, _port):
        self.con = (_ip, _port)
        self.buildSocketTCP()

    def buildSocketTCP(self):
        # Criando o canal de comunicação TCP entre client -> servidor
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect(self.con)

    
    
client = Client('localhost', 55555)

