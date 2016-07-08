from HexModel import *
from EventManager import EventManager

class HexBoardKI(HexModel):
    
    def setPlayer(self, player):
        self._player = player
    
    def getPlayer(self):
        return self._player
    
    # game finished event
    def onGameFinished(self):
        #EventManager.notify("KIGameFinished")
        self._finished = True
    