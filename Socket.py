import socket
import json
from datetime import datetime
from time import localtime, strftime


class Client:
    payload_size = 1024

    def __init__(self,host_to_connect,port_to_connect):
        self.host = host_to_connect
        self.port = port_to_connect

    def alterar_endereco(self,host,port):
        self.host = host
        self.port = port

    def connect_sock(self): # Cria e configura um socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        servidor = (self.host, self.port) # Endereço e Portas para se conectar
        print("Cliente conectando no endereço %s:%s " % servidor)
        return sock, servidor

    def connect_to_server(self,servidor,sock: socket.socket): # Conecta o socket em um servidor
        sock.settimeout(10) 
        sock.connect(servidor)
        sock.settimeout(None)
        return sock

    def connect_tcp(self):

        sock,servidor = Client.connect_sock(self)
        try:
            sock = Client.connect_to_server(self,servidor,sock)
            message = "test"
            sock.sendall(message.encode()) # Envia mensagem

            data = sock.recv(1024).decode()
            data = json.loads(data)

        except ConnectionError as e:
            print("Erro na conexão: %s" %str(e))
        except TimeoutError as te:
            print("Conexão não foi estabelecida em tempo adequado")
        finally:
            sock.close

class Server:
    payload_size = 1024
    
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def serverTCP_nuvem(self): #Receber requisições
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        servidor = (self.host, self.port)
        sock.bind(servidor)

        #print("Servidor iniciando no endereço %s:%s" % servidor)
        sock.listen(20) #escuta até 32 hidrometros diferentes
        sock.settimeout(120) 
        while True:
            try:
                #print ("Aguardando requisições de clientes...")
                client,adress = sock.accept() #Espera receber algum pacote json
                data = client.recv(self.payload_size) #Recebemos bytes de um Json encoded em utf-8
                if data:
                    
                    client_adress = client.getpeername()
                    client_ip = {"IP":client_adress[0]}

                    print(client_ip)                   

                    client.sendall(data) #Envia os dados para o hidrometro
                    client.close()

            except TimeoutError as errt: 
                print("O tempo de espera do servidor foi excedido! - %s" % errt)
                break

