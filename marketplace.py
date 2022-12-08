from flask import Flask, request
from collections import defaultdict
import os
import time
from threading import Thread
import json
import time
import p2pConfig as conf
from peer import Peer
import uuid
from vector import vector_clock
import concurrent.futures
from transaction import transaction as trs

main_marketplace = None


class Market:
    def __init__(self, host:str, port:int, name:str, id:int):
        self.id:uuid = uuid.uuid4()
        self.host:str = host
        self.port:int = port
        self.name:str = name
        self.peers:list = self.Generate_peer_list()
        self.lista_produtos:dict = defaultdict(dict)
        self.fila_transacao:list = list()
        self.fila_alteracao_produto:dict = defaultdict(dict)
        self.lamport_clock:vector_clock = vector_clock( id, 0)

    def Generate_peer_list(self):
        peer_list:list = list()
        r = range(self.port,self.port+conf.ALLOCATED_PORT_RANGE)
        for i in r:
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

    def transaction(self, product):
        transaction = trs(self.lamport_clock, product)
        #Transação é somente com produtos
        #Colocamos a nossa transação na nossa fila e a enviamos para outros marketplaces também a executar
        try:
            futures = None
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for peer in self.peers:
                    futures = [executor.submit(peer.sendTransaction, transaction)]
                # Tarefa para outros marketplaces procesarem a transação
                # Tarefa para o proprio marketplace processar a transação
            #print(f.result() for f in futures)
        except Exception as exp:
            print(exp)

                    
    def add_products(self, json):
        id = uuid.uuid1()
        self.lista_produtos[id].update({json}) # Errado, tem que ir pra fila de alteração
        return True
    
    def add_transaction(self, transaction): #Adiciona transação somente para este marketplace
        pass

    def enviar_product(self):
        #Utilizar os pares para enviar seus produtos para os peer, que enviarão para outros marketplaces
        pass

    def thread_fila_transacao(self):
        #Thread que executa os elementos na fila de transação
        pass
    def thread_fila_alteracao(self):
        #Thread que executa os elementos na fila de alteracao
        pass

app = Flask(__name__)
@app.route('/api', methods=['GET'])
def api():
    return "Marketplace Operando"

# Pesca
# /api/cadastro/?id=1&produto=Carro&qtd=3&preco=12&loja=Armario_seu_Kleber
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
            loja = str(args["loja"])
            product = f'{id} '
            main_marketplace.lista_produtos[id].update({"id":id})
            main_marketplace.lista_produtos[id].update({"produto":produto})
            main_marketplace.lista_produtos[id].update({"qtd":qtd})
            main_marketplace.lista_produtos[id].update({"preco":preco})
            main_marketplace.lista_produtos[id].update({"loja":loja})
            print(main_marketplace.lista_produtos)
            return "cadastrei "+qtd+" "+produto+" da  loja "+loja
    return "produto não informado"

# Consulta produtos do MarketPlace
@app.route('/api/mercadoria', methods=['GET'])
def api_produtos():
    args = request.args
    args = args.to_dict()

    if "id" in args:
        if args["id"] != "":
            id = str( args["id"])
            return main_marketplace.lista_produtos[id]
    elif "produto" in args:
        js = defaultdict(dict)
        i=0
        for key, value in main_marketplace.lista_produtos.items():
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
    return main_marketplace.lista_produtos

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
            main_marketplace.lista_produtos[id].update({"id":id})
            
            main_marketplace.lista_produtos[id].update({"host":host})
            main_marketplace.lista_produtos[id].update({"port":porta})
            return "Marketplace cadastrado"
    return  "Nenhum market place informado"

if __name__ == '__main__':

    x = {
            "id": str(uuid.uuid1()),
            "nome": "GPU",
            "qtd": 2,
            "preco": 3.5,
            "id_marketplace": str(uuid.uuid4()),
            "loja": "Jota Jota",
        }

    host= input("Informe o IP: ")
    port = int(input("Informe a Porta: "))
    nome = input("Informe o nome do marketplace: ")

    mkt = Market(host,port,nome, int(uuid.uuid1()) )
    main_marketplace = mkt
    try:
        sender = Thread(target=mkt.Generate_peer_list)
        tester = Thread(target=mkt.transaction, args=(x,))
        receiver = Thread(target=app.run, args=( host, port,))

        receiver.start()
        sender.start()
        time.sleep(5)
        tester.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        sender.join()
        tester.join()

