from tkinter import *

class MenuView:
    
    def __init__(self, master, GUI):        
        
        frame = Frame(master)
        frame.pack()
        
        self.GUI = GUI
        
        self.logoImage = PhotoImage(file="logo2.gif")
        self.logo = Label(master, image=self.logoImage)
        
        self.button = Button(frame, 
                             text="Beenden", fg="red",
                             command=frame.quit)
        
        self.Player1 = Button(frame,
                             text="Player 1 and start",
                             command=lambda: self.startGame(2))
        
        self.Player2 = Button(frame,
                             text="Player 2 and start",
                             command=lambda: self.startGame(1))
        
        self.Player0 = Button(frame,
                             text="Random Player and start",
                             command=lambda: self.startGame(0))
        
        self.winnerLabelText = StringVar()
        self.winnerLabel = Label(frame, textvariable=self.winnerLabelText)
        
        
    
    def won(self, winner):
        self.winnerLabelText.set("Spieler " + str(winner) + " hat gewonnen!")
    
    def startGame(self, player):
        self.GUI.Game.start(player)
        self.GUI.openPage("game")
    
    def show(self):
        self.logo.pack(side=LEFT)
        self.button.pack(side=LEFT)
        self.Player1.pack(side=LEFT)
        self.Player2.pack(side=LEFT)
        self.Player0.pack(side=LEFT)
        
        self.winnerLabel.pack(side=LEFT)
        
    def hide(self):
        self.logo.pack_forget()
        self.button.pack_forget()
        self.Player1.pack_forget()
        self.Player2.pack_forget()
        self.Player0.pack_forget()
        self.winnerLabelText.set("")
        self.winnerLabel.pack_forget()
    
    def draw(self):
        return 0
    