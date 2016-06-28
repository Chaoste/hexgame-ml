from tkinter import *
from HexagonPattern import HexagonPattern

class GameView:
    
    def __init__(self, master, GUI, game):        
        # Size of the Canvas Widget
        self.canvas_width = GUI.screenSize[0]
        self.canvas_height = GUI.screenSize[1]
        
        self.Game = game
        
        # Iniitate Canvas object and pack
        self.canvas = Canvas(master, width = self.canvas_width, height = self.canvas_height)
        
        self.canvas.bind("<Motion>", self.onMouseOver)
        self.canvas.bind("<Leave>", self.onMouseLeft)
        self.canvas.bind("<Button>", self.onClick)
        
        self.PlayerSwapButton = Button(master,
                             text="Swap Player",
                             command=self.swapPlayer)
        
        # Create Hexgame Interface
        self.Pattern = HexagonPattern(self)
        
        # Initial Drawing
        self.draw()
    
    def swapPlayer(self):
        self.Game.changePlayer()
        self.Game.HexBoard.switchColors()
        self.hidePlayerSwap()
        self.draw()
    
    def showPlayerSwap(self):
        self.PlayerSwapButton.pack()
    
    def hidePlayerSwap(self):
        self.PlayerSwapButton.pack_forget()
    
    def show(self):
        self.canvas.pack()
        
    def hide(self):
        self.canvas.pack_forget()
        self.hidePlayerSwap()
    
    def onMouseOver(self, event):
        self.Pattern.onMouseOver(event)
    
    def onMouseLeft(self, event):
        print("Mouse left canvas area")
    
    def onClick(self, event):
        move = self.Pattern.mapCoordToCell([event.x, event.y])
        self.Game.makeMove(move)
    
    def draw(self):
        self.Pattern.draw()
    