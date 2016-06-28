from KI import *
import random

class MainKI(KI):
    
    def __init__(self, game):
        super().__init__(game)
        
        self.Vertices = list(self.Game.HexBoard.Vertices.values())
    
    def getMove(self):
        
        random.shuffle(self.Vertices)
        vertex = self.Vertices.pop()
        
        return [vertex.j, vertex.i]