from flask import Flask, request
import paho.mqtt.client as mqtt
from random import randint
from collections import defaultdict
import os
import operator
import time
from threading import Thread
import codecs
from bs4 import BeautifulSoup
import json
from threading import Thread
import time

# Lista de produtos no consorcio de marketplaces
lista_produtos = defaultdict(dict)
# Lista de Marketplaces no consorcio 
lista_marketplaces = defaultdict(dict)
#fila de requisições
fila_de_comandos = defaultdict(dict)
pos=0
class marketplace:
    def __init__(self,host,port,name) -> None:
        self.id = randint(1,100)
        self.host = host
        self.port = port
        self.name = name

def comunicacao(self):
    while True:
       if pos != "0":
            print("replicando base de dados")
            for key, value in lista_marketplaces.items():
               URL = "https://"+value["host"]+":"+value["port"]+"/api/cadastro"
               PARAMS = ({"id":1},{"produto":"cadeira"},{"qtd":1},{"preco":120},{"idMP":self.id},{"loja":"loja"})
               req = request(url = URL, params= PARAMS)
            pos =0
       time.sleep(2)
    pass

app = Flask(__name__)
@app.route('/api', methods=['GET'])
def api():
    return "Marketplace Operando"

# Pesca
# /api/cadastro?id=1&produto=Carro&qtd=3&preco=12&idMP=1&loja=Armario_seu_Kleber
@app.route('/api/cadastro', methods=['GET'])
def api_cad():
    args = request.args
    args = args.to_dict()

    if "id" in args:
        if args["id"] != "":
            id = str(args["id"])
            produto = str(args["produto"])
            qtd = str(args["qtd"])
            preco = str(args["preco"])
            id_marketplace = str(args["idMP"])
            loja = str(args["loja"])
            lista_produtos[id].update({"id":id})
            lista_produtos[id].update({"nome":produto})
            lista_produtos[id].update({"qtd":qtd})
            lista_produtos[id].update({"preco":preco})
            lista_produtos[id].update({"id_marketplace":id_marketplace})
            lista_produtos[id].update({"loja":loja})
            pos = id
            return "Cadastrei "+qtd+" "+produto
    return "produto não informado"

# Consulta produtos do MarketPlace
@app.route('/api/produto', methods=['GET'])
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
    host1= input("Informe o host:")
    porta = input("Informe a porta:")
    nome = input("Informeo o nome do marketplace:")

    marketplace = marketplace(porta,host1,nome)
    
    api = Thread(target= app.run(host= host1, port=porta))
    com = Thread(target= comunicacao)
    api.start()
    com.start()