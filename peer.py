import socket
import time
import uuid
import p2pConfig as conf
import json
from enum import Enum
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, request
from threading import Thread
from transaction import transaction as trs


class Peer:
    def __init__(self,host:str, port:int, marketplace):
        self.id:uuid = uuid.uuid4()
        self.connection:set = set()
        self.SuccefullConnection:set = set()
        self.Host:str = host
        self.Port:int = port
        self.Market = marketplace
        self.Ocupado:bool = False

    def Add_connection(self, url:str):
        self.connection.add(url)

    def Del_connection(self, url:str):
        try:
            self.connection.remove(url)
        except Exception:
            print("URL não cadastrada")

    def ShowConnections(self):
        while True:
            print(self.SuccefullConnection)
            time.sleep(2)

    def ARP(self):
        self.Ocupado = True
        try:
            headers = {'content-type': 'application/json'}
        except Exception as exp:
            print(exp)
        try:
            for url in self.connection:
                for port in conf.PORT_RANGE:
                    if port < self.Market.port or port >= self.Market.port+conf.ALLOCATED_PORT_RANGE:
                        try:
                            link = f'http://{url}:{port}/api/connection'
                            my_info = (self.Host, self.Port)
                            peer_info = (url,str(port))
                            r = requests.post(link, json= my_info, headers= headers, timeout= 0.010, ) #Adiciona par encontrado na lista
                            print(f"Par encontrado em: {link} - {r.status_code}")
                            self.SuccefullConnection.add(peer_info)
                            r.close()
                        except requests.exceptions.ConnectionError as errc:
                            print(f"Falha ao conectar em :{port}")
                            pass
                        except requests.exceptions.Timeout as errt:
                            print("Timeout")
                            pass
                        except requests.exceptions.InvalidURL as erriu:
                            print("Invalid URL")
                            pass
                        except AssertionError as erae:
                            print("Peer type is incorrect")
                            pass
                        except Exception as exp:
                            print(exp)
                            pass
                print(f'Busca finalizada em: {url}')
        except Exception as MainFailure:
            print(MainFailure)
        
        self.Ocupado = False

    def sendMessage(self, msg):
        err = None
        headers = {'content-type': 'application/json'}
        for info in self.SuccefullConnection.copy():
            try:
                link = f'http://{info[0]}:{info[1]}/api/produto'
                r = requests.post(link,json= msg, headers=headers, timeout= 2)
                response = r.text
                r.close()
                print(f"Enviado com sucesso - {link}")
                return response
            except requests.exceptions.InvalidURL as erriu:
                print("Invalid URL")
                err = erriu
            except requests.exceptions.ConnectionError as errc:
                err = errc
                print(f"Não enviou - {link}")
            except Exception as exp:
                err = exp
                print(exp)        

    def sendTransaction(self, transaction:trs):
        headers = {'content-type': 'application/json'}
        for info in self.SuccefullConnection.copy():
            try:
                link = f'http://{info[0]}:{info[1]}/api/transaction'
                r = requests.post(link, json=transaction, headers=headers, timeout= 2)
                response = r.text
                r.close()
                print(f"Transação enviada com sucesso - {link}")
                return response
            except requests.exceptions.InvalidURL as erriu:
                print("Invalid URL")
                err = erriu
            except requests.exceptions.ConnectionError as errc:
                err = errc
                print(f"Transação não enviada - {link}")
            except Exception as exp:
                err = exp
                print(exp)              

Main_Peer:Peer = None

app = Flask(__name__)

@app.route('/api/connection', methods=['POST'])
def arp():
    args = request.data.decode() #Caso seja encontrado por um par
    print(f'Novo par encontrado: {args}')
    args = json.loads(args)
    Main_Peer.SuccefullConnection.add((args[0],args[1]))
    return "Success"

@app.route('/api/produto', methods=['GET', 'POST', 'PUT'])
def updateProdutoList():
    if request.method == 'GET':
        return f"Get - {request.host}"
        
    elif request.method == "POST":
        # Receber o request
        # Ler o Jason
        # Salvar Jason no marketplace cadastrado
        # Marketplace terá uma fila paea cadastro dos itens, com verificação de item duplicado
        # Se tudo foi realizado retorna um Yes
        return "Yes"
        
    elif request.method == "PUT":
        return "Put"
        
    return "Error"

@app.route('/api/transaction', methods=['GET', 'POST', 'PUT'])
def updateProduto(id_produto):
    if request.method == 'GET':
        pass
    elif request.method == "POST":
        #Main_Peer.Market.add_ #Esperar o marketplace resolver
        print(f"Transacao recebida! - {request.json}")
        return True
        
    elif request.method == "PUT":
        pass
    return "Error"

if __name__ == '__main__': #Teste
    from marketplace import Market
    x = {
            "id": str(uuid.uuid1()),
            "nome": "GPU",
            "qtd": 2,
            "preco": 3.5,
            "id_marketplace": str(uuid.uuid4()),
            "loja": "Jota Jota",
        }

    IP = input("Digite o IP: ")
    port = int(input("Digite a Porta: "))
    market = Market("localhost",port,"JotaJota")
    par = Peer(host=IP, port=port, marketplace=market)
    Main_Peer = par
    par.Add_connection("localhost")
    try:
        sender = Thread(target=par.ARP)
        receiver = Thread(target=app.run, args=( IP, port,))
        test = Thread(target=par.sendMessage, args=(x,))

        receiver.start()
        sender.start()
        test.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        sender.join()
        test.join()