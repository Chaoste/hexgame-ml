from Pattern import *

class SamplePattern(Pattern):
    
    def __init__(self, ki):
        super().__init__(ki)
        
        self.name = "SamplePattern"
    
    def check(self):
        
        self.PivotVertices = []
        
        for key, vertex in self.KI.Game.HexBoard.Vertices.items():
            
            
            if self.KI.Game.currentPlayer() == 1:
                player = 2
            else:
                player = 1
            
            if vertex.player == player:
                
                
                if (
                    self.KI.Game.HexBoard.getVertex(vertex.i + 1, vertex.j).player == player and
                    self.KI.Game.HexBoard.getVertex(vertex.i + 1, vertex.j - 2).player == player
                    ):
                    
                    self.PivotVertices.append(vertex)
        
        if len(self.PivotVertices) > 0:
            return True
        return False