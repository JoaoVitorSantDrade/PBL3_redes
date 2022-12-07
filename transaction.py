import uuid
from vector import vector_clock
class transaction:
    def __init__(self,clock:vector_clock):
        self.id:uuid = uuid.uuid4()
        self.clock:vector_clock = clock
        self.itens:dict = dict()
        self.status:int = 0
    
    def status_change(self,status:int):
        self.status=status

    def transaction_kill(self):
        del self
    
    