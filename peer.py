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


x={
    1: {
            "id": str(uuid.uuid1()),
            "nome": "GPU",
            "qtd": 2,
            "preco": 3.5,
            "id_marketplace": str(uuid.uuid4()),
            "loja": "Jota Jota",
        }
    
    }


class Peer:
    def __init__(self,host:str, port:int, Marketplace_Port:int):
        self.id:uuid = uuid.uuid4()
        self.connection:set = set()
        self.SuccefullConnection:set = set()
        self.Host:str = host
        self.Port:int = port
        self.MK_Port:int = Marketplace_Port
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

            retry = Retry(backoff_factor=0.005, connect=2)
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            headers = {'content-type': 'application/json'}
        except Exception as exp:
            print(exp)
        try:
            for url in self.connection:
                for port in conf.PORT_RANGE:
                    if port < self.MK_Port or port >= self.MK_Port+conf.ALLOCATED_PORT_RANGE:
                        try:
                            link = url + ":" + str(port)
                            my_info = (self.Host, self.Port)
                            peer_info = (url,str(port))
                            r = session.post(link + "/api/connection" , json=my_info, headers=headers, timeout=0.002) #Adiciona par encontrado na lista
                            print(f"Par encontrado em: {link} - {r.status_code}")
                            self.SuccefullConnection.add(peer_info)
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

    def sendMessage(self, j_data):
        while True:
            retry = Retry(backoff_factor=0.005, connect=2)
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            headers = {'content-type': 'application/json'}
            j_data = json.dumps(j_data)
            for info in self.SuccefullConnection.copy():
                try:
                    link = f'http://{info[0]}:{info[1]}'
                    r = session.post(link + "/api/produto",json=j_data, headers=headers, timeout=0.005)
                except requests.exceptions.InvalidURL as erriu:
                    print("Invalid URL")
                    pass
                except requests.exceptions.ConnectionError as errc:
                    print(f"Falha ao enviar mensagem em :{info[1]}")
                    pass
                except Exception as exp:
                    print(exp)
                    pass
                    

            time.sleep(2)

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
        return "Get"
        pass
    elif request.method == "POST":
        args = request.json
        print(f'{args} erro aqui?')
        return "Post"
        pass
    elif request.method == "PUT":
        return "Put"
        pass
    return "Error"

@app.route('/api/produto/<id_produto>', methods=['GET', 'POST', 'PUT'])
def updateProduto(id_produto):
    if request.method == 'GET':
        pass
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    return "Error"

if __name__ == '__main__': #Teste

    IP = input("Digite o IP: ")
    port = int(input("Digite a Porta: "))
    par = Peer(host=IP, port=port,Marketplace_Port=port)
    Main_Peer = par
    par.Add_connection("http://localhost")
    try:
        sender = Thread(target=par.ARP)
        receiver = Thread(target=app.run, args=("0.0.0.0",port,))
        test = Thread(target=par.sendMessage, args=(x))

        receiver.start()
        sender.start()
        test.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        sender.join()
        test.join()