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
        
        # 2 Bridge oben links
        self.addPattern("E0,0E,00,00;------x-;3;0;00000;5")
        
        # 2 Bridge oben
        self.addPattern("00E,000,0E0,000,000;------------x--;4;0;00000;5")
        
        # 2 Bridge oben rechts
        self.addPattern("000E,0E00,0000,0000;------------x---;3;0;00000;5")
        
        # 2 Bridge nach unten
        self.addPattern("?0E0,0000,0000;---------x--;2;1;00000;4")
        
        # eigene Steine zur Seite bringen // unten links
        self.addPattern("?0P,00?;----x-;1;0;00000;1")
        self.addPattern("00,0P;x---;0;0;00000;0")
        self.addPattern("?00,P0?;--x---;0;2;00000;0")
        self.addPattern("P0,00;---x;1;1;00000;0")
        
        
        
        #self.loadPatterns()
        
        self.Vertices = dict(self.Game.HexBoard.Vertices)
        
    
    def getMove(self):
        
        if self.Game.moveCounter <= 2:
            return [0, 0]
        
        else:
            
            # save game state
            self.GameState = self.mapGameState()
            
            # check for pattern occurence
            patterns = self.checkPatterns()
            
            if len(patterns) > 0:
                
                #patternToSelect = max(patterns, key=lambda x:x[0])
                patternToSelect = random.choice(patterns)
                
                i_shift = int(patternToSelect[1])
                j_shift = int(patternToSelect[2])
                i = int(patternToSelect[3])
                j = int(patternToSelect[4])
                
                print(i_shift, i, j_shift, j)
                
                print("Advising", [j_shift + j, i_shift + i], j_shift, j, i_shift, i)
                return [j_shift + j, i_shift + i]
            
            
            
            
            vertices = list(self.Game.HexBoard.Vertices.values())
            
            if len(vertices) > 0:
                
                shuffle(vertices)
                vertex = vertices.pop()
                return [vertex.j, vertex.i]
            
            else:
                return [0,0]
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def addPattern(self, text):
        modes = text.split(";")
        self.Patterns[modes[0]] = Pattern(len(modes[0].split(",")), len(modes[0].split(",")[0]), modes[0].replace(",", ""), modes[1], modes[2], modes[3], modes[4], modes[5])
    
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
        
        PatternsFound = []
        
        player = self.Game.currentPlayer()
        
        if player == 2:
            enemy = 1
        else:
            enemy = 2
        
        print("enemy is", enemy)
        translator = {"0": 0, "E": enemy, "e": enemy, "P": player, "p": player}
        
        for key, pattern in self.Patterns.items():
            
            # calc min shift left
            
            
            if player == 2:
                y0 = -pattern.topMargin
                yn = self.Game.size[0] - pattern.m + 1 + pattern.topMargin + pattern.bottomMargin
                
                x0 = -pattern.leftMargin
                xn = self.Game.size[1] - pattern.n + 1 + pattern.leftMargin + pattern.rightMargin
            else:
                x0 = -pattern.topMargin
                xn = self.Game.size[0] - pattern.m + 1 + pattern.topMargin + pattern.bottomMargin
                
                y0 = -pattern.leftMargin
                yn = self.Game.size[1] - pattern.n + 1 + pattern.leftMargin + pattern.rightMargin
                
            for i_shift in range(y0, yn):

                for j_shift in range(x0, xn):
                    
                    matching = True
                    
                    for i in range(pattern.m):
                        for j in range(pattern.n):
                                                        
                            
                            patternIndex = i * pattern.n + j
                            if player == 2:
                                globalIndex = (i_shift + i) * self.Game.size[0] + j_shift + j
                            else:
                                globalIndex = (j_shift + j) * self.Game.size[0] + i_shift + i
                            
                            #print(pattern.pattern, patternIndex, i, j, pattern.n)
                            
                            patternVal = pattern.pattern[patternIndex]
                            
                            if patternVal != "?" and len(self.GameState) > globalIndex and globalIndex >= 0:
                                
                                
                                
                                patternComp = str(translator[patternVal])
                                gameComp = str(self.GameState[globalIndex])
                                
                                
                                
                                #print(patternComp, gameComp)
                                
                                if patternVal == "e" and (gameComp == "0" or gameComp == patternComp):
                                    print("alternative enemy")
                                    
                                elif patternVal == "p" and (gameComp == "0" or gameComp == patternComp):
                                    print("alternative player")
                                                                    
                                elif patternComp != gameComp:
                                    matching = False
                                    break
                        
                    if matching == True:
                        print("Advise due to", pattern.pattern)
                        if player == 2:
                            PatternsFound.append([pattern.weight, i_shift, j_shift, pattern.i, pattern.j])
                        else:
                            PatternsFound.append([pattern.weight, j_shift, i_shift, pattern.i, pattern.j])
        
        return PatternsFound
    