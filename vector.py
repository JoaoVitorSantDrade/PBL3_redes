import p2pConfig as conf

class vector_clock:
    def __init__(self,id) -> None:
        self.id = id
        self.count = int(conf.MARKETPLACE_QUANTITY)
        self.clock = [0 for i in range(self.count)] #Teremos 10 posições, escolhemos isso como padrão do projeto

    def print_clock(self):
        print("relogio de:",self.id)
        print(self.clock)
        
    def update(self,sClock):
        i =0
        while( i< self.count):
            if( sClock[i] > self.clock[i]):
                self.clock[i] = sClock[i]
            i = i+1
        self.clock[int(self.id)] +=1 

    def event(self):
        id = int(self.id)
        self.clock[id] = self.clock[id] + 1

    def to_dict(self):
        x = {
            "id":self.id,
            "count":self.count,
            "clock":self.clock
        }
        return x

def main():
    ck1 = vector_clock(0,3)
    ck2 = vector_clock(1,3)
    ck3 = vector_clock(2,3)

    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck1.event()
    ck2.update(ck1.clock)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck1.event()
    ck2.update(ck1.clock)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck3.event()
    ck1.update(ck3.clock)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()
    
if __name__ == '__main__':
    main()
