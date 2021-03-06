from HexGUI import *
from HexBoard import HexBoard
import random
from EventManager import EventManager
from MachineGUI import MachineGUI

class Game:
    
    
    
    def __init__(self, m, n, mode):
        
        # init all events
        EventManager.initEvents()
        
        EventManager.subscribe("GameFinished", self.onGameFinished)
        EventManager.subscribe("GameStarted", self.onGameStarted)
        
        # save size and mode
        self.size = [m,n]
        self.mode = mode
        
        # just to init the value
        self._currentPlayer = 1
        
        # instantiate model and view
        self.HexBoard = HexBoard(self.size[0], self.size[1])
        self.HexBoard.setReferenceToGame(self)
        
        if self.UIRequired():
            self.HexGUI = HexGUI(self.size[0], self.size[1], self)
        else:
            self.MachineGUI = MachineGUI(self.size[0], self.size[1], self)
        
        # set the game to entry point
        self.start(self._currentPlayer)
        
        if self.UIRequired():
            # main loop starts for event receiving
            self.HexGUI.mainloop()
        
        if self.UIRequired() == False:
            self.MachineGUI.gameLoop()
            
    def UIRequired(self):
        if self.mode == "human" or self.mode == "ki" or self.mode == "inter":
            return True
        else:
            return False
    def start(self, firstPlayer):
        
        EventManager.notify("GameStarting")
        
        # move counter init
        self.moveCounter = 0
        
        # generate fresh state
        self.HexBoard = HexBoard(self.size[0], self.size[1])
        self.HexBoard.setReferenceToGame(self)
        
        # current player depending on decision
        self._currentPlayer = firstPlayer
        
        # if random number wanted, generate one
        if firstPlayer == 0:
            self.chooseFirst()
        
        EventManager.notify("GameStarted")
    
    def onGameStarted(self):
        
        if self.UIRequired():
            # draw the gui
            self.HexGUI.draw()
        
    # Game finished event
    def onGameFinished(self):
        
        if self.UIRequired():
            # move over to main menu and present the winner
            self.HexGUI.openPage("menu")
            self.HexGUI.won(self.HexBoard.winner())
    
    # generate random player number
    def chooseFirst(self):
        self._currentPlayer = round(random.random()) + 1
    
    # is the getter for the private variable
    def currentPlayer(self):
        return self._currentPlayer
    
    # alter the players
    def changePlayer(self):
        if self._currentPlayer == 1:
            self._currentPlayer = 2
        else:
            self._currentPlayer = 1
    
    # control flow for click event
    def makeMove(self, move):
        
        # Notify 
        EventManager.notify("MoveBegan")
        
        # if already marked dont do anything
        if self.HexBoard.isMarked(move[1], move[0]):
            EventManager.notify("MoveDenied")
            
        else:
            
            # otherwise count the click
            self.moveCounter = self.moveCounter + 1
            
            # notify Model
            self.HexBoard.receiveMove(move)
            
            # notify View
            self.changePlayer()
            EventManager.notify("PlayerChanged")
        
        EventManager.notify("MoveFinished")
        
        
        
        
        
        