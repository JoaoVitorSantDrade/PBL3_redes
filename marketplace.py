from flask import Flask, request
from collections import defaultdict
from threading import Thread
import p2pConfig as conf
from peer import Peer
import peer as fullPeer
import uuid
from vector import vector_clock
from transaction import transaction as trs

main_marketplace = None


class Market:
    def __init__(self, host:str, port:int, name:str, id:int):
        self.id:uuid = uuid.uuid4()
        self.host:str = host
        self.port:int = port
        self.name:str = name
        self.peers:list = None
        self.lista_produtos:dict = defaultdict(dict)
        self.fila_transacao:list = list()
        self.fila_alteracao_produto:dict = defaultdict(dict)
        self.lamport_clock:vector_clock = vector_clock(int(id))

    #Gera os Pares do marketplace
    def Generate_peer_list(self):
        peer_list:list = list()
        connection_set = set()
        FirstTime = True
        r = range(self.port + 1,self.port+conf.ALLOCATED_PORT_RANGE)
        for i in r:
            new_peer = Peer(self.host,port= i,marketplace=self,connections= FirstTime)
            print(f'Par {i} foi gerado')
            if FirstTime == True:
                connection_set = new_peer.ShowConnections()
                FirstTime = False
            else:
                new_peer.connection = connection_set  
    
            peer_server = Thread(target=fullPeer.Peer_run_server, args=( new_peer,), daemon=True)
            peer_server.start()
                
            peer_list.append(new_peer)
        self.peers = peer_list

    # Envia uma transação para outros marketplaces, e a si mesmo.
    def transaction(self, product):
        transaction = trs(self.lamport_clock, product)

        #Transação é somente com produtos
        #Colocamos a nossa transação na nossa fila e a enviamos para outros marketplaces também a executar
        try:
            threads = [] #Threads a serem abertas
            for peer in self.peers:
                # Tarefa para outros marketplaces procesarem a transação
                t = Thread(target=peer.sendTransaction, args=(transaction,))
                t.start()
                threads.append(t)
            # Tarefa para o proprio marketplace processar a transação
            self_t = Thread(target=self.add_transaction, args=(transaction,))
            self_t.start()
            threads.append(self_t)
            for aux in threads:
                aux.join()
        except Exception as exp:
            print(exp)
        

                    
    def add_products(self, json):
        id = uuid.uuid1()
        self.lista_produtos[id].update({json}) # Errado, tem que ir pra fila de alteração
        return True
    
    def add_transaction(self, product:trs): #Adiciona transação somente para este marketplace
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
# /api/cadastro/?produto=Carro&qtd=3&preco=12&loja=Armario_seu_Kleber
@app.route('/api/cadastro/', methods=['GET'])
def api_cad():
    args = request.args
    args = args.to_dict()
    
    if "produto" in args:
        if args["produto"] != "":
            nome_produto = str(args["produto"])
            qtd_produto = int(args["qtd"])
            preco_produto = str(args["preco"])
            loja = str(args["loja"])
            x = {
                "id": int(uuid.uuid1()),
                "nome": nome_produto,
                "qtd": qtd_produto,
                "preco": preco_produto,
                "id_marketplace": main_marketplace.id,
                "loja": loja,
            }

            main_marketplace.transaction(x) #Fila de transações ainda não implementada! ByPass abaixo
            main_marketplace.lista_produtos[x[id]].update(x) 

            return f"cadastrei {qtd_produto}x {nome_produto} em: {loja} [{x['id_marketplace']}]"
    return "produto não informado"

# Consulta TODOS produtos do MarketPlace
# /api/mercadoria
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
@app.route('/api/transaction', methods=['POST'])
def ap_transaction_makertplace():
    print(request.json)
    return  "Nenhum market place informado"


def test():

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
    mkt.Generate_peer_list()
    main_marketplace = mkt
    try:
        tester = Thread(target=mkt.transaction, args=(x,))
        receiver = Thread(target=app.run, args=( host, port,))

        receiver.start()
        tester.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        tester.join()

def main():
   
    host= input("Informe o IP: ")
    port = int(input("Informe a Porta: "))
    nome = input("Informe o nome do marketplace: ")

    mkt = Market(host,port,nome, int(uuid.uuid1()) )
    mkt.Generate_peer_list()
    global main_marketplace
    main_marketplace = mkt
    try:
        receiver = Thread(target=app.run, args=( host, port,))

        receiver.start()

    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()

if __name__ == '__main__':
    main()

