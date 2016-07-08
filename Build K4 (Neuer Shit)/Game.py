from HexGUI import *
from HexBoard import HexBoard
import random
from EventManager import EventManager
from MachineGUI import MachineGUI
from HexKI import *
class Game:
    
    
    
    def __init__(self, m, n, mode):
        
        # init all events
        EventManager.initEvents()
        
        EventManager.subscribe("GameFinished", self.onGameFinished)
        EventManager.subscribe("GameStarted", self.onGameStarted)
        EventManager.subscribe("MoveFinished", self.onMoveFinished)
        EventManager.subscribe("GameUILoaded", self.onGameUILoaded)
        EventManager.subscribe("ToggleVictoryPath", self.onToggleVictoryPath)
        
        self._pause = False
        
        # save size and mode
        self.size = [m,n]
        self.mode = mode
        
        # just to init the value
        self._currentPlayer = 1
        self._currentPlayerType = "human"
        
        # instantiate model and view
        self.HexBoard = HexBoard(self.size[0], self.size[1])
        self.HexBoard.setReferenceToGame(self)
        
        self.GameState = 0
        
        self.moveCounter = 0
        
        if self.UIRequired():
            self.HexGUI = HexGUI(self.size[0], self.size[1], self)
        else:
            self.MachineGUI = MachineGUI(self.size[0], self.size[1], self)
        
        if self.mode == "ki":
            self.KI = HexKI(self.size[0], self.size[1])
        
        if self.mode == "inter" or self.mode == "machine":
            
            self.KI = []
            self.KI.append(HexKI(self.size[0], self.size[1]))
            self.KI.append(HexKI(self.size[0], self.size[1]))
            
            self._currentPlayerType = "ki"
        
        # set the game to entry point
        #self.start(self._currentPlayer)
        
        
        
        if self.UIRequired():
            
            EventManager.subscribe("UITick", self.onUITick)
            
            # main loop starts for event receiving
            self.HexGUI.mainloop()
        
        if self.UIRequired() == False:
            self.GameState = 1
            self.MachineGUI.gameLoop()
        
        
        
    
    def onUITick(self):
        self.doKIMove()
        
    def onToggleVictoryPath(self):
        
        if self.UIRequired():
            vertices = self.HexBoard.getVictoryPath()
            self.HexGUI._GUIGameBoard.Pattern.toggleVictoryPath(vertices)
        
    def pause(self):
        self._pause = not self._pause
       
    def UIRequired(self):
        if self.mode == "human" or self.mode == "ki" or self.mode == "inter":
            return True
        else:
            return False
    
    def start(self, firstPlayer):
        
        self.GameState = 0
        
        EventManager.notify("GameStarting")
        
        # move counter init
        self.moveCounter = 0
        
        # generate fresh state
        self.HexBoard = HexBoard(self.size[0], self.size[1])
        self.HexBoard.setReferenceToGame(self)
        
        # current player depending on decision
        self._currentPlayer = firstPlayer
        
        if self.mode == "ki":
            self.KI = HexKI(self.size[0], self.size[1])
        
        if self.mode == "inter" or self.mode == "machine":
            
            self.KI = []
            self.KI.append(HexKI(self.size[0], self.size[1]))
            self.KI.append(HexKI(self.size[0], self.size[1]))
            
            self._currentPlayerType = "ki"
        
        # if random number wanted, generate one
        if firstPlayer == 0:
            self.chooseFirst()
        
        EventManager.notify("GameStarted")
    
    def onGameStarted(self):
        
        self.GameState = 1
        
        if self.UIRequired():
            # draw the gui
            self.HexGUI.draw()
        
        
    # Game finished event
    def onGameFinished(self):
        
        self.GameState = 0
        
        if self.UIRequired():
            # move over to main menu and present the winner
            self.HexGUI.openPage("menu")
            self.HexGUI.won(self.HexBoard.winner())
    
    
    
    def onGameUILoaded(self):
        pass
        #if self.mode == "inter" or (self.mode == "ki" and self._currentPlayerType == "human"):
        #    print("IM KI")
            
    
    # generate random player number
    def chooseFirst(self):
        self._currentPlayer = round(random.random()) + 1
    
    # is the getter for the private variable
    def currentPlayer(self):
        return self._currentPlayer
    
    # is the current Player human?
    def isPlayerHuman(self):
        return self._currentPlayerType == "human"
    
    # alter the players
    def changePlayer(self):
        
        if self._currentPlayer == 1:
            self._currentPlayer = 2
            
        else:
            self._currentPlayer = 1
            
        if self.mode == "ki":
            
            if self._currentPlayerType == "human":
                self._currentPlayerType = "ki"
            else:
                self._currentPlayerType = "human"
        
        if self.mode in ["inter", "machine"]:
            
            self._currentPlayerType = "ki"
                
    
    # control flow for click event
    def makeMove(self, move):
                
        # Notify 
        EventManager.notify("MoveBegan")
        
        # if already marked dont do anything
        if self.HexBoard.isMarked(move[0], move[1]):
            EventManager.notify("MoveDenied")
            
        else:
            
            # otherwise count the click
            self.moveCounter = self.moveCounter + 1
            
            # notify Model
            self.HexBoard.receiveMove(move)
            
            if self.mode == "inter":
                self.KI[0].receiveMove(move)
                self.KI[1].receiveMove(move)
            elif self.mode == "ki":
                self.KI.receiveMove(move)
            
            # notify View
            self.changePlayer()
            EventManager.notify("PlayerChanged")
            
            
            
        EventManager.notify("MoveFinished")
    
    
    def doKIMove(self):
        
        if self.GameState == 1:
            
            if not self.isPlayerHuman() and self.mode == "ki":
                move = self.KI.nextMove()
                self.makeMove(move)
    
            elif self.mode == "inter" or self.mode == "machine":
                move = self.KI[self.currentPlayer()-1].nextMove()
                #print(move, self.currentPlayer())
                #print("making", move)
                self.makeMove(move)
            
    def onMoveFinished(self):
        pass
        
        
        