from tkinter import *
import random
import collections
from EventManager import EventManager
from random import shuffle


class MachineGUI:
    
    def __init__(self, m, n, game):
        self.size = [m,n]
        self.Game = game
        
        self._finished = False
        
        self.targetIterations = 5000   
        self.q = 0 
        
        print("MachineGUI loaded")
    
    
    WonVertices = []
    IterationCounter = 0
    
        
    def gameLoop(self):
        
        while self.IterationCounter < self.targetIterations:
            
            vertices = list(self.Game.HexBoard.Vertices.values())
            
            while len(vertices) > 0:
                
                shuffle(vertices)
                vertex = vertices.pop()
            
                self.Game.makeMove([vertex.j, vertex.i])
            
            self.IterationCounter = self.IterationCounter + 1
            
            for key, value in self.Game.HexBoard.Vertices.items():
                if value.player == self.Game.HexBoard.winner():
                    self.WonVertices.append(str(value.i) + ";" + str(value.j))
            
            if self.IterationCounter // (self.targetIterations / 20) != self.q:
                self.q = self.IterationCounter // (self.targetIterations / 20)
                print(round(self.IterationCounter/self.targetIterations * 100,1), "%", self.IterationCounter)
            
            self.Game.start(1)
        
        print(collections.Counter(self.WonVertices))


        
    def receiveMove(self, move):
        # do somehting
        return 0
    
    def won(self, winner):
        print("won")