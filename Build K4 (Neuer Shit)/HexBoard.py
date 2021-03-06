from HexModel import HexModel
from SimulationHexBoard import SimulationHexBoard
from EventManager import EventManager

class HexBoard(HexModel):

    def setReferenceToGame(self, game):

        # game reference
        self.Game = game

        self._player = self.Game.currentPlayer()

    def getPlayer(self):

        return self.Game.currentPlayer()

    # game finished event
    def onGameFinished(self):
        EventManager.notify("GameFinished")
        self._finished = True

    def copy(self):
        return SimulationHexBoard(self)
