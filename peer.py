import uuid
import p2pConfig as conf
import requests
from flask import Flask, request
from threading import Thread
from transaction import transaction as trs

Main_Peer = None

class Peer:
    def __init__(self,host:str, port:int, marketplace, connections:bool = True):
        self.id:uuid = uuid.uuid4()
        self.connection:set = set()
        self.SuccefullConnection:set = set()
        self.Host:str = host
        self.Port:int = port
        self.Market = marketplace
        self.Add_connection(conf.DEFAULT_HOST) #Adiciona um host padrão (Localhost)
        self.Initialized = False
        if connections == True:
            self.ARP() #Busca outros Peers

    def Add_connection(self, url:str):
        self.connection.add(url)

    def Del_connection(self, url:str):
        try:
            self.connection.remove(url)
        except Exception:
            print("URL não cadastrada")

    def ShowConnections(self):
            return self.SuccefullConnection

    def ARP(self):
        try:
            headers = {'content-type': 'application/json'}
        except Exception as exp:
            print(exp)
        try:
            for url in self.connection:
                for port in conf.PORT_RANGE:

                    port_str = str(port-10000)
                    marketplaces_present = "0" in port_str

                    if port < self.Market.port or port >= self.Market.port+conf.ALLOCATED_PORT_RANGE and not marketplaces_present:
                        if port != 10000:
                            try:
                                link = f'http://{url}:{port}/api/connection'
                                my_info = (self.Host, self.Port)
                                peer_info = (url,str(port))
                                r = requests.post(link, json= my_info, headers= headers, timeout= 0.005, ) #Adiciona par encontrado na lista
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
        
    def sendMessage(self, msg):
        err = None
        headers = {'content-type': 'application/json'}
        for info in self.connection:
            for port in conf.PORT_RANGE:

                    port_str = str(port-10000)
                    marketplaces_not_present = "0" in port_str

                    if port < self.Market.port or port >= self.Market.port+conf.ALLOCATED_PORT_RANGE and marketplaces_not_present:
                        try:
                            link = f'http://{info[0]}:{info[1]}/api/produto'
                            r = requests.post(link,json= msg, headers=headers, timeout= 2)
                            response = r.text
                            r.close()
                            print(f"Enviado com sucesso - {link} - {r.status_code}")
                            #return response
                        except requests.exceptions.InvalidURL as erriu:
                            print("Invalid URL")
                            err = erriu
                        except requests.exceptions.ConnectionError as errc:
                            err = errc
                            print(f"Não enviou - {link}")
                        except Exception as exp:
                            err = exp
                            print(exp)        

    def sendToMarket(self, transaction):
        headers = {'content-type': 'application/json'}
        link = f'http://{self.Market.host}:{self.Market.port}/api/transaction'
        r = requests.post(link, json=transaction, headers=headers, timeout = 1)
        response = r.text
        r.close()


    def sendTransaction(self, transaction:trs):
        headers = {'content-type': 'application/json'}
        resposta = []
        for info in self.SuccefullConnection:
            try:
                link = f'http://{info[0]}:{info[1]}/api/transaction' 
                r = requests.post(link, json=transaction.to_dict(), headers=headers, timeout= 2)
                response = r.text
                r.close()
                resposta.append(response)
            except requests.exceptions.InvalidURL as erriu:
                print("Invalid URL")
                err = erriu
            except requests.exceptions.ConnectionError as errc:
                err = errc
                print(f"Transação não enviada - {link}")
            except Exception as exp:
                err = exp
                print(exp)
                return "Error"
        return resposta


app = Flask(__name__)

@app.route('/api/connection', methods=['POST'])
def arp():
    args = request.json #Caso seja encontrado por um par
    print(f'Par tentou se conectar: {args}')
    try:
        global Main_Peer
        Main_Peer
        Main_Peer.SuccefullConnection.add((args[0],args[1]))
        print(f'Par se conectou: {args}')
        return f"Conexão com {args} feita com sucesso", 201

    except Exception as exp:
        print(exp)
        return "Erro", 500

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
        return "Success", 201
        
    elif request.method == "PUT":
        return "Put"
        
    return "Error"

@app.route('/api/transaction', methods=['GET', 'POST', 'PUT'])
def updateProduto():
    if request.method == 'GET':
        return "request.json", 200
    elif request.method == "POST":
        #Passar transação p/ marketplace processar
        print(f"Transacao recebida! - {request.host_url}")
        Main_Peer.sendToMarket(request.json)
        return f"Sucesso - {request.host}", 201
        
    elif request.method == "PUT":
        pass
    return "Error"

def Peer_run_server(peer:Peer):
    global Main_Peer
    Main_Peer = peer
    peer_server = Thread(target=app.run, args=( Main_Peer.Host, Main_Peer.Port,))
    peer_server.start()
    peer_server.join()    
    return

def test():
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
    market = Market("localhost",port,"JotaJota", 2)
    par = Peer(host=IP, port=port, marketplace=market)
    par.Add_connection("localhost")
    global Main_Peer
    Main_Peer = par
    try:
        receiver = Thread(target=app.run, args=( IP, port,))
        test = Thread(target=par.sendMessage, args=(x,))

        receiver.start()
        test.start()


    except Exception as expt:
        print(expt)
        
    finally: 
        receiver.join()
        test.join()


if __name__ == '__main__': #Teste
    test()