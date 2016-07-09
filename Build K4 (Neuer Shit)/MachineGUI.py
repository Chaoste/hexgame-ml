from tkinter import *
import random
import collections
from EventManager import EventManager
from random import shuffle
from HexKI import HexKI
from HexBoard import HexBoard


class MachineGUI:
    
    def __init__(self, m, n, game):
        self.size = [m,n]
        self.Game = game
        
        EventManager.subscribe("GameFinished", self.onGameFinished)
        
        self._finished = False
        
        self.targetIterations = 20
        self.q = 0 
        
        self.start()
        
        
        print("MachineGUI loaded")
    
    def start(self):
        
        self.KI = []
        self.KI.append(HexKI(self.size[0], self.size[1]))
        self.KI.append(HexKI(self.size[0], self.size[1]))
        
        self.Game.HexBoard = HexBoard(self.size[0], self.size[1])
        self.Game.HexBoard.setReferenceToGame(self.Game)
    
    WonVertices = []
    IterationCounter = 0
    
        
    def gameLoop(self):
        
        print("Entering Game Loop")
        player = 1
        Q = []
        while self.IterationCounter < self.targetIterations:
            
            q= 0
            while not self._finished:

                q += 1
                if player == 0:
                    player = 1
                else:
                    player = 0
                
                move = self.KI[player].nextMove()
                
                self.KI[0].receiveMove(move)
                self.KI[1].receiveMove(move)
                self.Game.makeMove(move)
                
                #print(self.KI[player].PatternMatcher.mapGameState())
            
            if q < 50:
                Q.append(q)
            self.IterationCounter = self.IterationCounter + 1
            
            
            
            for key, value in self.Game.HexBoard.Vertices.items():
                if value.player == self.Game.HexBoard.winner():
                    self.WonVertices.append(str(value.i) + ";" + str(value.j))
            
            if self.IterationCounter // (self.targetIterations / 20) != self.q:
                self.q = self.IterationCounter // (self.targetIterations / 20)
                print(round(self.IterationCounter/self.targetIterations * 100,1), "%", self.IterationCounter)
            
            self.Game.HexBoard = HexBoard(self.size[0], self.size[1])
            self.Game.HexBoard.setReferenceToGame(self.Game)
            
            self._finished = False
            self.start()
            
        print("FINISHED")
        
        f = open('output.txt', 'r+')
        f.write("Move Count: Average:" + str(round(sum(Q) / len(Q))) + ", Min:", str(min(Q)) + ", Max:" + str(max(Q)) + str(Q))
        
        
        print(collections.Counter(self.WonVertices))

    def onGameFinished(self):
        #print("Spieler", self.Game.HexBoard.winner(), "hat gewonnen!")
        self._finished = True
        
    def receiveMove(self, move):
        # do somehting
        return 0
    
    def won(self, winner):
        print("won")