import uuid
from vector import vector_clock

class transaction:
    def __init__(self,clock:vector_clock, item:dict):
        self.id:uuid = uuid.uuid4()
        self.clock:vector_clock = clock
        self.itens:dict = item
        self.type:int = 0 # 0 Transação comum | 1 Adicionar produto | 2 Remover Produto | 3 Apagar Produto
        self.status:int = 0
    
    def status_change(self,status:int):
        self.status=status

    def transaction_kill(self):
        del self
    
    def to_dict(self):
        x = {
            "id": str(self.id),
            "clock":self.clock.to_dict(), #olhar isso
            "item":self.itens,
            "type":self.type,
            "status":self.status
        }
        return x