from tkinter import *

class SplashScreenView:
    
    def __init__(self, master, GUI):  
        
        
        logoImage = PhotoImage(file="logo2.gif")
        self.logo = Label(master, image=logoImage)
        
        self.logo.bind("<Button>", self.openMenu)
        
              
        self.GUI = GUI
    
    def openMenu(self, event):
        self.GUI.openPage("menu")
    
    def show(self):
        self.logo.pack()
        
    def hide(self):
        self.logo.pack_forget()
    
    def draw(self):
        return 0