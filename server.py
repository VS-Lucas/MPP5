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
        sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckt.bind(self.con)
        sckt.listen(2)
        self.client1, self.addr1 = sckt.accept()
    
        print('Primeiro usuário conectado')

    def sendfile(self) -> None:
        pathsize = os.path.getsize(self.file)
        self.client1.sendall(bytes(f'Enviando arquivo: {self.file} | {pathsize} bytes', 'utf-8'))

        with open(self.file, 'rb') as file:
            byte_data = file.read(self.BUFFER)
            startTime = time.time()
            while byte_data:
                self.cont += 1
                print(f'Pacote: {self.cont} | {pathsize} bytes restantes para o upload')
                self.client1.send(byte_data)
                byte_data = file.read(self.BUFFER)
        print('Arquivo enviado com sucesso!')

        self.taxaPerdaUp  = pathsize / 56427430
        self.uploadTime   = time.time() - startTime
        self.receivedDataUp   = 56427430 - pathsize
        self.taxaVazaoUP      = (self.receivedData)/(self.downloadTime)

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
        self.msg = self.client1.recvfrom(1024)
        self.size = int(self.msg[0].split()[4].decode())
        self.file = self.msg[0].split()[2].decode()

        with open(self.file, 'wb') as file:
            byte_data = self.client1.recv(self.BUFFER)
            self.size -= self.BUFFER
            startTime = time.time()
            try:
                while self.size > 0:
                    self.cont += 1
                    print(f'Pacote: {self.cont} | {self.size} bytes restantes para o dowload')
                    file.write(byte_data)
                    byte_data = self.client1.recvfrom(self.BUFFER)[0]
                    self.size -= self.BUFFER
            except:
                print('ERROR')
        self.downloadTime     = time.time() - startTime
        self.taxaPerdaDown    = self.size / 56427430
        self.receivedDataDown   = 56427430 - self.size
        self.taxaVazaoDown      = (self.receivedData)/(self.uploadTime)
        print('Arquivo recebido')
        file.close()
 
client = Server('192.168.0.84', 55555, 100)
