from Observer import Observer

class User(Observer):   
    def __init__(self, name,id=None):
        super().__init__()
        self.id = id
        self.name = name
    
    # def register(self,password):
    #     pass
    #
    # def login(self):
    #     pass
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name