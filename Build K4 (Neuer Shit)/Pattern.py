class Pattern:
    
    def __init__(self, m, n, pattern, target, i, j, flagMask, weight = 0):
        
        self.m = m
        self.n = n
        self.i = i
        self.j = j
        self.pattern = pattern
        self.target = target
        self.flagMask = flagMask
        self.weight = weight
        
        self.margins = self.getMargins()
    
    #@abstractmethod
    def check(self):
        return 0
    
    
    def getMargins(self):
        
        marginLiterals = ["0", "?", "p", "e"]
        
        # left, right, top, bottom
        
        # check left
        stop = False
        for col in range(self.n):
            for row in range(self.m):
                if self.pattern[row * self.n + col] not in marginLiterals:
                    self.leftMargin = col
                    stop = True
                    break
            if stop:
                break
        
        # check right
        stop = False
        for col in range(self.n):
            for row in range(self.m):
                if self.pattern[row * self.n + (self.n-1-col)] not in marginLiterals:
                    self.rightMargin = col
                    stop = True
                    break
            if stop:
                break
        
        # check top
        stop = False
        for row in range(self.m):
            for col in range(self.n):
                if self.pattern[row * self.n + col] not in marginLiterals:
                    self.topMargin = row
                    stop = True
                    break
            if stop:
                break
        
        # check bottom
        stop = False
        for row in range(self.m):
            for col in range(self.n):
                if self.pattern[(self.m-1-row) * self.n + col] not in marginLiterals:
                    self.bottomMargin = row
                    stop = True
                    break
            if stop:
                break
        
        self.i = int(self.i)
        self.j = int(self.j)
        
        # where is the new value set??
        if self.i > self.m - self.bottomMargin:
            self.bottomMargin = self.m - self.i -1
        
        if self.i - self.topMargin < 0:
            self.topMargin = self.i 
        
        if self.j > self.n - self.rightMargin:
            self.rightMargin = self.n - self.j -1
        
        if self.j - self.leftMargin < 0:
            self.leftMargin = self.j