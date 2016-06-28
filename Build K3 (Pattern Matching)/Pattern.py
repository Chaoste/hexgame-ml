class Pattern:
    
    def __init__(self, ki):
        
        self.name = ""
        self.KI = ki
        self.importance = 0
    
    #@abstractmethod
    def check(self):
        return 0