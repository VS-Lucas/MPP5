import socket
import os
import time

class Client:
    def __init__(self, _ip: str, _port: int, _path: str, _buffer: int) -> None:
        self.con = (_ip, _port)
        self.path = _path
        self.BUFFER = _buffer
        self.cont = 0
        self.buildSocketUDP()
        self.sendfile()
        self.recvfile()

    def buildSocketUDP(self) -> None:
        # Criando o canal de comunicação TCP entre client -> servidor
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sckt.connect(self.con)

    def sendfile(self) -> None:
        pathsize = os.path.getsize(self.path)
        print(pathsize)
        self.sckt.sendto(bytes(f'Enviando arquivo: {self.path} | {pathsize} bytes', 'utf-8'), self.con)

        with open(self.path, 'rb') as file:
            byte_data = file.read(self.BUFFER)
            pathsize -= self.BUFFER            
            try:
                startTime = time.time()
                while pathsize > 0:
                    self.cont += 1
                    print(f'Pacote: {self.cont} | {pathsize} bytes restantes para o upload')
   
                    self.sckt.sendto(byte_data, self.con)
                    byte_data = file.read(self.BUFFER)
                    pathsize -= self.BUFFER
            except:
                print('ERROR')
                
        self.taxaPerdaUp  = pathsize / 56427430
        self.uploadTime   = time.time() - startTime
        self.receivedDataUp   = 56427430 - pathsize
        self.taxaVazaoUP      = (self.receivedData)/(self.downloadTime)
        print('Arquivo enviado com sucesso!!')
    
    def recvfile(self) -> None:
        pathsize = os.path.getsize(self.path)
        self.sckt.recv(1024)
        with open('server.pdf', 'wb') as file:
            byte_data = self.sckt.recv(self.BUFFER)
            pathsize -= self.BUFFER
            startTime = time.time()
            while pathsize > 0:
                self.cont += 1
                print(f'Pacote: {self.cont} | {pathsize} bytes restantes para o dowload')
                file.write(byte_data)
                byte_data = self.sckt.recv(self.BUFFER)
                pathsize -= self.BUFFER
                
        self.downloadTime     = time.time() - startTime
        self.taxaPerdaDown    = pathsize / 56427430
        self.receivedDataDown   = 56427430 - pathsize
        self.taxaVazaoDown      = (self.receivedData)/(self.uploadTime)
        print('Arquivo recebido!!')
        file.close()

        self.TCP()
    
    def TCP(self):
        self.scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scktTCP.connect(self.con)
        
        self.scktTCP.sendall(bytes(f'{self.taxaPerdaUp} {self.taxaVazaoUP} {self.uploadTime}', 'utf-8'))
        
        self.scktTCP.sendall(bytes(f'{self.taxaPerdaDown} {self.taxaVazaoDown} {self.downloadTime}', 'utf-8'))
        
        data = self.scktTCP.recv(1024).decode()
        TaxaPerdaDown, VazaoDown, TempoDown = data.split()
        print(f'Taxa de perda do upload Cliente -> Servidor: {self.taxaPerdaUp*100}')
        print(f'Vazão do upload Cliente -> Servidor: {self.taxaVazaoUP}')
        print(f'Tempo de upload Cliente -> Servidor: {self.uploadTime}\n')
     
        print(f'Taxa de perda de download do Servidor: {TaxaPerdaDown*100}')
        print(f'Vazão de download do Servidor: {VazaoDown}')
        print(f'Tempo de download do Servidor: {TempoDown}')
        
        data = self.scktTCP.recv(1024).decode()
        TaxaPerdaUp, VazaoUp, TempoUp = data.split()
        print(f'Taxa de perda do upload Servidor -> Client: {TaxaPerdaUp*100}')
        print(f'Vazão do upload Servidor -> Cliente: {VazaoUp}')
        print(f'Tempo de upload Servidor -> Cliente: {TempoUp}\n')
     
        print(f'Taxa de perda de download do Cliente: {self.taxaPerdaDown*100}')
        print(f'Vazão de download do Cliente: {self.taxaVazaoDown}')
        print(f'Tempo de download do Cliente: {self.downloadTime}')
        pass
    
    def status(self):    
        pass

client = Client('179.152.253.19', 55555, "path-54MB.txt", 100)

