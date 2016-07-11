from HexModel import HexModel
from copy import deepcopy

class SimulationHexBoard(HexModel):

    def __init__(self, hexBoard):
        self.size = hexBoard.size
        self._groupCounter = hexBoard._groupCounter
        self._player = hexBoard._player
        self._finished = hexBoard._finished
        self.Vertices = deepcopy(hexBoard.Vertices)

    def receiveMove(self, move):
        super().receiveMove(move)
        if self._player == 1:
            self._player = 2
        else:
            self._player = 1

    def getPlayer(self):
        return self._player

    # game finished event
    def onGameFinished(self):
        self._finished = True

    def copy(self):
        return type(self)(self)
