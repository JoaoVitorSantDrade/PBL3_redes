
class vector_clock:
    def __init__(self,id,count) -> None:
        self.id = id
        self.clock = [0 for i in range(count)]
        self.count = count

    def print_clock(self):
        print("relogio de:",self.id)
        print(self.clock)
        
    def update(self,sClock):
        i =0
        while( i< self.count):
            if( sClock.clock[i] > self.clock[i]):
                self.clock[i] = sClock.clock[i]
            i = i+1
        self.clock[int(self.id)] +=1 
    def event(self):
        id = int(self.id)
        self.clock[id] = self.clock[id] + 1

def main():
    ck1 = vector_clock(0,3)
    ck2 = vector_clock(1,3)
    ck3 = vector_clock(2,3)

    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck1.event()
    ck2.update(ck1)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck1.event()
    ck2.update(ck1)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()

    ck3.event()
    ck1.update(ck3)

    print("\nApós aplicar lamport")
    ck1.print_clock()
    ck2.print_clock()
    ck3.print_clock()
    
if __name__ == '__main__':
    main()
