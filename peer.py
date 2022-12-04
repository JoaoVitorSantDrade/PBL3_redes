import socket
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
    def __init__(self, type:Peer_Type):
        self.id:uuid = uuid.uuid4()
        self.connection:list = list()
        self.type:Peer_Type = type

    def Add_connection(self, url:str):
        self.connection.append(url)

    def Del_connection(self, url:str):
        self.connection.remove(url)

    def Try_send(self, item:dict):
        try:
            assert self.type == Peer_Type.SENDER

            session = requests.Session()
            retry = Retry(connect=1, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            for url in self.connection:
                for i in conf.PORT_RANGE:
                    url = url + ":" + str(i)
                    print(url)
                    r = session.post(url, data="test".encode())
                    print(r.status_code)
                    print(r.headers)

        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.InvalidURL as erriu:
            print(erriu)
        except AssertionError as erae:
            print("Peer type is incorrect")
        except Exception as exp:
            pass

app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    print(request.data)


if __name__ == '__main__':
    par = Peer(Peer_Type.SENDER)
    par.Add_connection("https://localhost")
    par.Add_connection("https://google.com")
    msg = {"id": "01","quantity": "5","name": "GPU","marketplace": "Americanas","price": "1000"}
    try:
        sender = Thread(target=par.Try_send, args=(msg,))
        receiver = Thread(target=app.run, args=("0.0.0.0",10250,))

        sender.start()
        receiver.start()
    except Exception as expt:
        print(expt)
