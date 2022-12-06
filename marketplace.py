from flask import Flask, request
from random import randint
from collections import defaultdict
import os
import time
from threading import Thread
import json
import time
import p2pConfig as conf
from peer import Peer
import uuid

main_marketplace = None


class Market:
    def __init__(self, host:str, port:int, name:str):
        self.id:uuid = uuid.uuid4()
        self.host:str = host
        self.port:int = port
        self.name:str = name
        self.peers:list = self.Generate_peer_list()
        self.lista_produtos:dict = defaultdict(dict)
        main_marketplace = self

    def Generate_peer_list(self):
        peer_list:list = list()
        r = range(self.port,self.port+conf.ALLOCATED_PORT_RANGE)
        for i in r:
            print(i)
            new_peer = Peer(self.host,i,self)
            peer_list.append(new_peer)
        return peer_list

    def peer_comm(self, msg):
        for peer in self.peers:
            peer:Peer
            try:
                if not peer.Ocupado:
                    peer.sendMessage(msg=msg)
            except Exception as NotAvailableNow:
                print("Nenhum peer disponível, tente mais tarde")
                
    def add_products(self, json):
        id = uuid.uuid1()
        self.lista_produtos[id].update({json})
    
    def enviar_product(self):
        #Utilizar os pares para enviar seus produtos para os peer, que enviarão para outros marketplaces
        pass



app = Flask(__name__)
@app.route('/api', methods=['GET'])
def api():
    return "Marketplace Operando"

# Pesca
# /api/cadastro/?id=1&produto=Carro&qtd=3&preco=12&idMP=1&loja=Armario_seu_Kleber
@app.route('/api/cadastro/', methods=['GET'])
def api_cad():
    args = request.args
    args = args.to_dict()
    lista = main_marketplace.lista_produtos
    if "id" in args:
        if args["id"] != "":
            id = str(args["id"])
            produto = str(args["produto"])
            qtd = str(args["qtd"])
            preco = str(args["preco"])
            id_marketplace = str(args["idMP"])
            loja = str(args["loja"])
            product = f'{id} '
            return f'Foram cadastrado(s) {qtd} {produto}'
    return "produto não informado"

# Consulta produtos do MarketPlace
@app.route('/api/mercadoria', methods=['GET'])
def api_produtos():
    args = request.args
    args = args.to_dict()

    if "id" in args:
        if args["id"] != "":
            id = str( args["id"])
            return lista_produtos[id]
    elif "produto" in args:
        js = defaultdict(dict)
        i=0
        for key, value in lista_produtos.items():
            if value["nome"] == str(args["produto"]):
                x={
                    "id": key,
                    "nome": value["nome"],
                    "qtd": value["qtd"],
                    "preco": value["preco"],
                    "id_marketplace":value["id_marketplace"],
                    "loja": value["loja"],
                }
                js[str(i)].update(x)
                i = i + 1
        return js
    return lista_produtos

# Cadastra MarketPlaces
@app.route('/api/marketplaces/cadastro', methods=['GET'])
def ap_cad_makertplace():
    args = request.args
    args = args.to_dict()

    if "id" in args:
        if args["id"] !="":
            id = str( args["id"])
            host = str( args["host"])
            porta = str(args["port"])
            lista_marketplaces[id].update({"id":id})
            lista_marketplaces[id].update({"host":host})
            lista_marketplaces[id].update({"port":porta})
            return "Marketplace cadastrado"
    return  "Nenhum market place informado"

@app.route('/api/marketplaces', methods=['GET'])
def ap_makertplace():
    args = request.args
    args = args.to_dict()

    if "id" in args:
        if args["id"] !="":
            id = str( args["id"])
            return lista_marketplaces[id]
    return lista_marketplaces


if __name__ == '__main__':
    host= input("Informe o IP: ")
    port = int(input("Informe a Porta: "))
    nome = input("Informe o nome do marketplace: ")

    mkt = Market(host,port,nome)
    
    try:
        sender = Thread(target=mkt.Generate_peer_list)
        receiver = Thread(target=app.run, args=( host, port,))

        receiver.start()
        sender.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        sender.join()

