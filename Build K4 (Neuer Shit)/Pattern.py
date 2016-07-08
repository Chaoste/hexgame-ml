class Pattern:
    
    def __init__(self, reverse, pattern, weight = 0):
        
        self.m = len(pattern.split(","))
        self.n = len(pattern.split(",")[0])
        
        self.pattern = "".join(pattern.split(","))
        
        self.weight = weight
        
        if reverse:
            
            Q = []
            oldPattern = self.pattern
            for j in range(self.n):
                
                s = []
                for i in range(self.m):
                    s.append(self.pattern[i*self.n + j])
                
                #s.reverse()
                Q.append("".join(s))
            #Q.reverse()
            
            self.pattern = "".join(Q)
            
            m = self.m
            self.m = self.n
            self.n = m
            
            #self.getMargins()
            
            #print("GOT NEW inverted pattern", self.m, self.n, oldPattern, self.pattern)

        
        self.i = self.pattern.index("x") // self.n
        self.j = self.pattern.index("x") % self.n
        
        self.getMargins()
    
    def getMargins(self):
        
        marginLiterals = ["0", "?", "p", "e", "-"]
        
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
        if self.i >= self.m - self.bottomMargin:
            self.bottomMargin = self.m - self.i -1
        
        if self.i - self.topMargin < 0:
            self.topMargin = self.i 
        
        if self.j >= self.n - self.rightMargin:
            self.rightMargin = self.n - self.j -1
        
        if self.j - self.leftMargin < 0:
            self.leftMargin = self.j