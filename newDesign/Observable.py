from Observer import Observer

class Observable:
    def __init__(self):
        self.observers : list[Observer] = []
        
    def subscribe(self, observer : Observer):
        self.observers.append(observer)
    
    def unsubscribe(self, observer : Observer):
        self.observers.remove(observer)
    
    def notify(self,msg):
        for obs in self.observers:
            obs.update(msg)
        