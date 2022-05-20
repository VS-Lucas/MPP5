import socket
import os
import time
class Server:
    def __init__(self, _ip: str, _port: int, _buffer: int) -> None:
        self.con = (_ip, _port)
        self.BUFFER = _buffer
        self.cont = 0
        self.buildSocketUDP()
        self.recvfile()
        self.sendfile()
        

    def buildSocketUDP(self):
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sckt.bind(self.con)
        # sckt.listen()
        # self.client1, self.addr1 = sckt.accept()
    
        print('Primeiro usuário conectado')

    def sendfile(self) -> None:
        pathsize = os.path.getsize(self.file)
        self.sckt.sendto(bytes(f'Enviando arquivo: {self.file} | {pathsize} bytes', 'utf-8'), ('168.196.41.100', 55555))

        with open(self.file, 'rb') as file:
            byte_data = file.read(self.BUFFER)
            pathsize -= self.BUFFER
            startTime = time.time()
            while pathsize > 0:
                self.cont += 1
                print(f'Pacote: {self.cont} | {pathsize} bytes restantes para o upload')
                self.sckt.sendto(byte_data, ('168.196.41.100', 55555))
                byte_data = file.read(self.BUFFER)
                pathsize -= self.BUFFER
        print('Arquivo enviado com sucesso!')

        self.taxaPerdaUp  = pathsize / 220322835
        self.uploadTime   = time.time() - startTime
        self.receivedDataUp   = 220322835 - pathsize
        self.taxaVazaoUP      = (self.receivedDataUp)/(self.uploadTime)

        self.buildSocketTCP()
    
    def buildSocketTCP(self):
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.bind(self.con)
        self.client2, self.addr2 = sckt.accept()

        data = self.client2.recv(1024).decode()
        TaxaPerdaUpload, VazaoUpload, TempoUpload = data.split()
        print(f'Taxa de perda do upload Cliente -> Servidor: {TaxaPerdaUpload*100}')
        print(f'Vazão do upload Cliente -> Servidor: {VazaoUpload}')
        print(f'Tempo de upload Cliente -> Servidor: {TempoUpload}\n')
     
        print(f'Taxa de perda de download do Servidor: {self.taxaPerdaDown*100}')
        print(f'Vazão de download do Servidor: {self.taxaVazaoDown}')
        print(f'Tempo de download do Servidor: {self.downloadTime}')
        
        data = self.client2.recv(1024).decode()
        TaxaPerdaDown, VazaoDown, TempoDown = data.split()
        print(f'Taxa de perda do upload Servidor -> Client: {self.taxaPerdaUp*100}')
        print(f'Vazão do upload Servidor -> Cliente: {self.taxaVazaoUP}')
        print(f'Tempo de upload Servidor -> Cliente: {self.uploadTime}\n')
     
        print(f'Taxa de perda de download do Cliente: {TaxaPerdaDown*100}')
        print(f'Vazão de download do Cliente: {VazaoDown}')
        print(f'Tempo de download do Cliente: {TempoDown}')

        self.client2.sendall(bytes(f'{self.taxaPerdaDown} {self.taxaVazaoDown} {self.downloadTime}', 'utf-8'))
        self.client2.sendall(bytes(f'{self.taxaPerdaUp} {self.taxaVazaoUP} {self.uploadTime}', 'utf-8'))
        
        
    
    def recvfile(self) -> None:
        self.msg = self.sckt.recvfrom(1024)
        self.size = int(self.msg[0].split()[4].decode())
        self.file = self.msg[0].split()[2].decode()

        with open(self.file, 'wb') as file:
            byte_data = self.sckt.recv(self.BUFFER)
            self.size -= self.BUFFER
            startTime = time.time()
            try:
                while byte_data:
                    self.cont += 1
                    # if self.size <= 166000000:
                    #     break
                    print(f'Pacote: {self.cont} | {self.size} bytes restantes para o dowload')
                    file.write(byte_data)
                    byte_data = self.sckt.recvfrom(self.BUFFER)[0]
                    self.size -= self.BUFFER
            except:
                print('ERROR')
        # self.sckt.sendto('qqrcoisa', ('168.196.41.100', 55555))
        self.downloadTime     = time.time() - startTime
        self.taxaPerdaDown    = self.size / 220322835
        self.receivedDataDown   = 220322835 - self.size
        self.taxaVazaoDown      = (self.receivedDataDown)/(self.downloadTime)
        print('Arquivo recebido')
        file.close()
 
client = Server('192.168.0.84', 55555, 1024)
