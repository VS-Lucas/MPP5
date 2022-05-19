import socket



class Client:
    def __init__(self, _ip, _port):
        self.con = (_ip, _port)
        self.buildSocketUDP()

    def buildSocketUDP(self):
        # Criando o canal de comunicação UDP entre client -> servidor
        sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckt.connect(self.con)

client = Client('localhost', 55555)