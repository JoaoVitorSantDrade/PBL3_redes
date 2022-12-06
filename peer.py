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


class Peer_Type(Enum):
    UNDEFINED = 0
    SENDER = 1
    RECIEVER = 2

class Peer:
    def __init__(self, type:Peer_Type,host:str, port:int, Marketplace_Port:int):
        self.id:uuid = uuid.uuid4()
        self.connection:set = set()
        self.SuccefullConnection:set = set()
        self.type:Peer_Type = type
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
            assert self.type == Peer_Type.SENDER

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
                for i in conf.PORT_RANGE:
                    if i < self.MK_Port or i >= (self.MK_Port+30):
                        try:
                            link = url + ":" + str(i)
                            my_info = (self.Host, self.Port)
                            peer_info = (url,str(i))
                            r = session.post(link + "/api/connection" , json=my_info, headers=headers, timeout=0.002) #Adiciona par encontrado na lista
                            print(f"Par encontrado em: {link} - {r.status_code}")
                            self.SuccefullConnection.add(peer_info)
                        except requests.exceptions.ConnectionError as errc:
                            print(f"Falha ao conectar em :{i}")
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
                    
        except Exception as MainFailure:
            print(MainFailure)
        
        self.Ocupado = False

    def sendMessage(self, msg):
        pass

Main_Peer:Peer = None

app = Flask(__name__)

@app.route('/api/connection', methods=['POST'])
def arp():
    args = request.data.decode() #Caso seja encontrado por um par
    print(f'Novo par encontrado: {args}')
    args = json.loads(args)
    Main_Peer.SuccefullConnection.add((args[0],args[1]))
    return "Success"


if __name__ == '__main__': #Teste

    IP = input("Digite o IP: ")
    port = int(input("Digite a Porta: "))
    par = Peer(Peer_Type.SENDER, host=IP, port=port,Marketplace_Port=10030)
    Main_Peer = par
    par.Add_connection("http://localhost")
    try:
        sender = Thread(target=par.ARP)
        receiver = Thread(target=app.run, args=("0.0.0.0",port,))

        receiver.start()
        sender.start()

    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        sender.join()