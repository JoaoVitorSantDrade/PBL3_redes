from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import uuid
from random import randint

class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host =="localhost":
            host = "127.0.0.1"

        self.id = uuid.uuid4()
        self.address = (host, port)
        self._address = None
        self.server = ('127.0.0.1', 9999)
        print(f'My ID is: {self.id}\nMy Address is: {self.address}') 

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)

    def datagramReceived(self, datagram: bytes, addr):
        print("test")
        datagram = datagram.decode("utf-8")
        print(datagram)
        if addr == self.server: 
            print("Choose a client from:\n", datagram)
            self._address = input("Write host: "), int(input("Write port:"))
            print("entrou")
            reactor.callInThread(self.send_message)
        else:
            print(addr, ":", datagram)

    def send_message(self):
        while True:
            self.transport.write(input(":::").encode('utf-8'), self._address)

if __name__ == "__main__":
    port = randint(1000,5000)
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()