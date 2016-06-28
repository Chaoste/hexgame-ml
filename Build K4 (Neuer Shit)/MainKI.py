from KI import *
import random
from random import shuffle

class MainKI(KI):
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- General Interface --------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def __init__(self, game):
        super().__init__(game)
        
        self.FirstMove = [-1,-1]
        
        self.Vertices = dict(self.Game.HexBoard.Vertices)
    
    def getMove(self):
        
        if self.Game.moveCounter <= 2:
            self.FirstMove = self.calcFirstMove()
            return self.FirstMove
        
        else:
            return self.calcMove()
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def calcFirstMove(self):
        
        
        
        # pick a central vertex
        row = self.Game.size[0] // 2
        col = self.Game.size[1] // 2

        if self.Game.HexBoard.isMarked(row, col):
            Vertices = self.Game.HexBoard.getSurroundingVertices(row, col, 0)
            
            
            
            return [Vertices[0].j, Vertices[0].i]
        return [row, col]
    
    def calcMove(self):
        
        precision = 5
        
        for iteration in range(precision):
            
            DataSet = []
            
            for i in range(self.Game.size[0]):
                for j in range(self.Game.size[1]):
                    
                    if iteration == 0:
                        
                        Vertex = self.Vertices[str(i) + "," + str(j)]
                        
                        if Vertex.player == self.Game.currentPlayer():
                            Vertex.weight = 0
                            
                        elif Vertex.player != None and Vertex.player != self.Game.currentPlayer():
                            Vertex.weight = 0.5 # 1000
                            
                        else:
                            Vertex.weight = 0
                        
                    else:
                        Vertices = self.getSurroundingVertices(i, j)
                        
                        weight = 0
                        for vertex in Vertices:
                            weight += vertex.weight
                        
                        self.Vertices[str(i) + "," + str(j)].weight = weight
                    
                        DataSet.append([i, j, weight])
        
        L = []
        
        MidScale = 1000000
        
        for vertex in DataSet:
            
            if self.Vertices[str(vertex[0]) + "," + str(vertex[1])].player == None:
                
                weight = vertex[2]
                
                if self.Game.currentPlayer() == 1:
                        
                    midVal = abs(vertex[1] - (self.Game.size[1]) /2) * MidScale
                    
                else:
                    midVal = abs(vertex[0] - (self.Game.size[0]) /2) * MidScale
                
                x = weight
                weight = (midVal *(-1)) + (abs((self.Game.size[1]) /2) * MidScale) + weight
                #print("j", vertex[1], weight)
                
                L.append([vertex[0], vertex[1], x, weight])
                
        L = sorted(L, reverse=True, key=lambda x: x[2])
        #print(L)
        
        return [L[0][1],L[0][0]]
        
        
    # get all surrounding vertices
    # that are marked by the same player
    def getSurroundingVertices(self, i, j, player = -1):
        
        # hold an empty list to store the items in
        Q = []
        
        # some math stuff to mathematically get
        # a representation of the surrounding fields
        # to avoid the eye cancer of a bunch of loops
        for v in range(3):
            for w in range(2):
                
                # check this stuff on a piece of paper
                # to hard to describe
                r = v-1
                s = w
                s = (s * (1 - (abs(r) * 0.5)) * 2) - 1
                
                if r == 1:
                    s = s * (-1)
            
                s = s *(-1)
                r = j - int(r)
                s = i - int(s)
                
                if r >= 0 and r < self.Game.size[1] and s  >= 0 and s < self.Game.size[0]:
                    
                    
                    # get the vertex at that position    
                    vertex = self.Vertices[str(s)+","+str(r)]
                    
                    Q.append(vertex)
        
        return Q           
        
        
        
        
        
    
        
    
    
    
    
    