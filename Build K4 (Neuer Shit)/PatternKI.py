from KI import *
from Pattern import *

import random
from random import shuffle

class PatternKI(KI):
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- General Interface --------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def __init__(self, game):
        super().__init__(game)
        
        self.FirstMove = [-1,-1]
        
        self.PatternFile = "Patterns.txt"
        self.Patterns = {}
        self.loadPatterns()
        
        self.Vertices = dict(self.Game.HexBoard.Vertices)
        
    
    def getMove(self):
        
        if self.Game.moveCounter <= 2:
            return [0, 0]
        
        else:
            
            # save game state
            self.GameState = self.mapGameState()
            
            # check for pattern occurence
            patterns = self.checkPatterns()
            print(max(patterns.items(), key=lambda x:x.weight))
            
            
            return [0, 0]
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def loadPatterns(self):
        
        textFile = open(self.PatternFile, "r").read()
        
        for pattern in textFile.split("#"):
            modes = pattern.split(";")
            self.Patterns[modes[0]] = Pattern(len(modes[0].split(",")), len(modes[0].split(",")[0]), modes[0].replace(",", ""), modes[1], modes[2], modes[3], modes[4], modes[5])
    
    def mapGameState(self):
        
        gameState = ""
        
        for i in range(self.Game.size[0]):
            for j in range(self.Game.size[1]):
                
                vertex = self.Game.HexBoard.getVertex(i,j)
                
                player = vertex.player
                if vertex.player == None:
                    player = 0
                    
                gameState += str(player)
        
        return gameState
    
    def checkPatterns(self):
        
        PatternsFound = {}
        
        player = self.Game.currentPlayer()
        
        if player == 2:
            enemy = 1
        else:
            enemy = 2
        
        translator = {"0": 0, "1": enemy, "2": player}
        
        for key, pattern in self.Patterns.items():
            
            for i_shift in range(self.Game.size[0] - pattern.m + 1):
                for j_shift in range(self.Game.size[1] - pattern.n + 1):
                    
                    matching = True
                    i_0 = i_shift * self.Game.size[0] + j_shift
                    
                    for i in range(pattern.m):
                        for j in range(pattern.n):
                                                        
                            
                            patternIndex = i * pattern.m + j
                            globalIndex = (i_shift + i) * self.Game.size[0] + j_shift + j
                            
                            patternVal = pattern.pattern[patternIndex]
                            
                            if patternVal != "?":
                                
                                if str(translator[patternVal]) != str(self.GameState[globalIndex]):
                                    matching = False
                                    break
                        
                    if matching == True:
                        PatternsFound[pattern.pattern] = i_0
        
        return PatternsFound
    