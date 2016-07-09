from Pattern import *

import random
from random import shuffle

class PatternMatcher:
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- General Interface --------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def __init__(self, model, ki):
        
        self.Model = model
        self.KI = ki
        
        self.FirstMove = [-1,-1]
        
        self.Patterns = {}
        
        # 2 Bridge oben links
        self.addPattern("E0,0E,00,x0;0")
        
        # 2 Bridge oben blocken
        self.addPattern("00E,000,0E0,000,x00;0")
        
        # 2 Bridge oben rechts blocken
        self.addPattern("000E,0E00,0000,x000;0")
        
        # 2 Bridge nach unten blocken
        self.addPattern("?0E0,0000,0x00;0")
        
        # eigene Steine zur Seite bringen // unten links
        self.addPattern("?0P,x0?;1")
        self.addPattern("?0x,P0?;1")
        self.addPattern("P0,0x;1")
        
        #JannisBrückenbauenamanfang
        self.addPattern("x00,0P0,00P;1")
        self.addPattern("P00,0P0,00x;1")
        self.addPattern("??00x,00P0?,P00??;1")
        self.addPattern("??00P,?0P00,x00??;1")
              
        #JannisBrückenverhindern
        self.addPattern("00x0,??00,?0E0,?00?,0E0?;2")
        self.addPattern("0E,xP;3")
        self.addPattern("xP,E0;3")
        
        #JannisBrückenbauenspeziale
        self.addPattern("P,x,P;2")
        
        # Brücken schließen
        #self.addPattern("0P,P0;x---;0;0;00000;0")
        self.addPattern("0xP,P00;2.5")#<--- WERT GEÄNDERT
        self.addPattern("P0,xP;2.5")#<--- WERT GEÄNDERT
        #brücken schließen,wenn der gegner den anderen stein, der die brücke schließt gelegt hat.
        self.addPattern("Px,EP;3")
        self.addPattern("PE,xP;3")
        self.addPattern("?P,Ex,P?;0")
        self.addPattern("?P,xE,P?;0")
        self.addPattern("?xP,PE?;3")
        self.addPattern("?EP,Px?;3")
        
        # 1- Brücke verhindern
        self.addPattern("?E?,Px?,E??;0")
        
        # Gegner blockieren, selber brücke bauen
        self.addPattern("00P,E00,x00;0")
        
        # 2 bridge connecten
        self.addPattern("P0?,0x0,?0P;0")
        
        self.Vertices = dict(self.Model.Vertices)
        
    
    def getMove(self):
        
        # save game state
        self.GameState = self.mapGameState()

        # check for pattern occurence
        patterns = self.checkPatterns()
        
        if len(patterns) > 0:
            
            patternToSelect = max(patterns, key=lambda x:x[0])
            #patternToSelect = random.choice(patterns)
            
            i_shift = int(patternToSelect[1])
            j_shift = int(patternToSelect[2])
            i = int(patternToSelect[3])
            j = int(patternToSelect[4])
            
            #print("Pattern Used:", patternToSelect[5])
            
            return [i_shift + i, j_shift + j]
        
        else:
            return False
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    
    def addPattern(self, text):
        
        modes = text.split(";")
        
        if self.KI.getPlayer() == 1:
            reverse = False
        else:
            reverse = True
        
        self.Patterns[modes[0]] = Pattern(reverse, modes[0], modes[1])
    
    def mapGameState(self):
        
        gameState = ""
        
        for i in range(self.Model.size[0]):
            for j in range(self.Model.size[1]):
                
                vertex = self.Model.getVertex(i,j)
                
                player = vertex.player
                if vertex.player == None:
                    player = 0
                    
                gameState += str(player)
        
        return gameState
    
    def checkPatterns(self):
        
        PatternsFound = []
        
        player = self.KI.getPlayer()
        
        if player == 2:
            enemy = 1
        else:
            enemy = 2
        
        #print("enemy is", enemy)
        translator = {"x": 0, "0": 0, "E": enemy, "e": enemy, "P": player, "p": player}
        
        for key, pattern in self.Patterns.items():
            
            # calc min shift top
            y0 = -pattern.topMargin
            yn = self.Model.size[0] - pattern.m + 1 + pattern.topMargin + pattern.bottomMargin
                
            x0 = -pattern.leftMargin
            xn = self.Model.size[1] - pattern.n + 1 + pattern.leftMargin + pattern.rightMargin
                
            for i_shift in range(y0, yn):

                for j_shift in range(x0, xn):
                    
                    matching = True
                    
                    for i in range(pattern.m):
                        for j in range(pattern.n):
                                                        
                            
                            patternIndex = i * pattern.n + j
                            if player == 2:
                                globalIndex = (i_shift + i) * self.Model.size[0] + j_shift + j
                            else:
                                globalIndex = (j_shift + j) * self.Model.size[0] + i_shift + i
                            
                            #print(pattern.pattern, patternIndex, i, j, pattern.n)
                            
                            patternVal = pattern.pattern[patternIndex]
                            
                            if patternVal != "?":
                                
                                # border detection
                                if patternVal == "-":
                                    if (i_shift + i > self.KI.Size.m or i_shift + i < 0 or j_shift + j > self.KI.Size.n or j_shift + j < 0):
                                        pass
                                    else:
                                        matching = False
                                        break
                                    
                                elif len(self.GameState) > globalIndex and globalIndex >= 0:
                                    
                                    
                                    
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
                                
                                
                        
                    if matching == True and not self.Model.isMarked(i_shift + pattern.i, j_shift + pattern.j):
                        
                        PatternsFound.append([pattern.weight, i_shift, j_shift, pattern.i, pattern.j, pattern.pattern])
        
        return PatternsFound
    