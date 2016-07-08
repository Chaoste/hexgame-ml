from BinaryPattern import *

class BinaryPatterns:
    
    def __init__(self):
        
        self.patterns = []
        
    def readFile(self):
        
        file = open("binaryPatterns.txt", "r")
        str = file.read()
        
        items = str.split("#")
        
        for pattern in items:
            print(pattern)
            q = pattern.split(",")
            self.patterns.append(BinaryPattern(q[0], [q[1], q[2]]))
            
        self.patterns = sorted(self.patterns, reverse=True, key=lambda x:x.weight)
        
        #print(self.patterns)
    
    def mapToInt(self, dictOfVertices, currentPlayer):

        friend = 0b0
        enemy = 0b0
        
        for i, vertex in dictOfVertices.items():
            if vertex.player == currentPlayer:
                friend = (friend << 1) + 0b1
                enemy = (friend << 1) + 0b0
            else:
                friend = (friend << 1) + 0b0
                enemy = (friend << 1) + 0b1
                
            
            mask = (friend << len(dictOfVertices)) + enemy
        
        return mask
    
    def parse(self, dictOfVertices, currentPlayer):
        
        mask = self.mapToInt(dictOfVertices, currentPlayer)
        patternsFound = []
        
        maskBefore = 0
        for pattern in self.patterns:
            
            #print("Checking", mask, pattern.mask)
            
            if len(patternsFound) > 0 and pattern.mask != mask:
                break
            
            if pattern.mask == mask:
                patternsFound.append(pattern)
        
        return sorted(patternsFound, reverse=True, key=lambda x:x.weight)
    
    









# 1011101
# 1 0 1 1 1 0 1 1

# 7,7kB

gameBoard = "1200021000021000000"

# 



        