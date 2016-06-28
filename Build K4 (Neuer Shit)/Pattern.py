class Pattern:
    
    def __init__(self, m, n, pattern, i, j, target, flagMask, weight = 0):
        
        self.m = m
        self.n = n
        self.i = i
        self.j = j
        self.pattern = pattern
        self.target = target
        self.flagMask = flagMask
        self.weight = weight
    
    #@abstractmethod
    def check(self):
        return 0