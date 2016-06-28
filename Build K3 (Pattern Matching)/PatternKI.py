from KI import *
from SamplePattern import SamplePattern

import random
from random import shuffle

class PatternKI(KI):
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- General Interface --------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def __init__(self, game):
        super().__init__(game)
        
        self.FirstMove = [-1,-1]
        
        
        self.Vertices = dict(self.Game.HexBoard.Vertices)
        
        self.initPatterns()
    
    def getMove(self):
        
        if self.Game.moveCounter <= 2:
            self.FirstMove = self.calcFirstMove()
            return self.FirstMove
        
        else:
            return self.calcMove()
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    Patterns = []
    ApplicablePatterns = []
    
    def initPatterns(self):
        
        # Sample Pattern hinzufügen
        self.Patterns.append(SamplePattern(self))
        
        
        
    def checkPatterns(self):
        
        self.ApplicablePatterns = []
        
        for pattern in self.Patterns:
            if pattern.check():
                self.ApplicablePatterns.append(pattern)
                
    
    def calcFirstMove(self):
        
        
        
        # pick a central vertex
        row = self.Game.size[0] // 2
        col = self.Game.size[1] // 2

        if self.Game.HexBoard.isMarked(row, col):
            Vertices = self.Game.HexBoard.getSurroundingVertices(row, col, 0)
            
            
            
            return [Vertices[0].j, Vertices[0].i]
        return [row, col]
    
    i = 0
    def calcMove(self):
        
        self.checkPatterns()
        if len(self.ApplicablePatterns) > 0:
            
            pattern = max(self.ApplicablePatterns, key= lambda x:x.importance)
            
            print("Pattern", pattern.name, "detected. It's weight: ", pattern.importance)
        
        self.i = self.i + 1
        return [0,self.i]
        