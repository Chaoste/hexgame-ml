from Hexagon import *
from EventManager import EventManager
#Hex Board enthält die Game Logik und speichert die States

class HexBoard:
    
    def __init__(self, m, n):
        
        self.size = [m, n]
        
        # subscribe to certain events
        EventManager.subscribe("GameFinished", self.onGameFinished)
        
        # keep track, increment on each added vertex
        self._groupCounter = 2
        
        # bool to determine machine state
        self._finished = False
        
        # dictionary for all vertices
        self.Vertices = {}
        
        for i in range(m):
            for j in range(n):
                # add Hexagon instance to the dict
                # with key => i;j
                self.Vertices[str(i) + "," + str(j)] = Hexagon(i, j)
        
    def setReferenceToGame(self, game):
        self.Game = game
    
    # vertex is clicked
    def isMarked(self, i, j):
        
        state = self.getVertex(i, j).player
        
        if state == None:
            return False
        else:
            return True
    
    # get Vertex at certain index
    def getVertex(self, i, j):
        return self.Vertices[str(i) + "," + str(j)]
    
    # return machine state
    def finished(self):
        return self._finished
    
    # in case of a won game
    # return last player
    def winner(self):
        self.Game.changePlayer()
        return self.Game.currentPlayer()
        if self.finished() ==  True:
            print(self.Game.currentPlayer())
            self.Game.currentPlayer()
    
    # get all surrounding vertices
    # that are marked by the same player
    def getSurroundingVertices(self, i, j):
        
        # hold an empty list to store the items in
        Q = []
        
        # some math stuff to mathematically get
        # a representation of the surrounding fields
        # to avoid the eye cancer of a bunch of loops
        for v in range(3):
            for w in range(2):
                
                # check this stuff on a piece of paper
                # to hard to describe
                r = v-1
                s = w
                s = (s * (1 - (abs(r) * 0.5)) * 2) - 1
                
                if r == 1:
                    s = s * (-1)
            
                s = s *(-1)
                r = j - int(r)
                s = i - int(s)
                
                if r >= 0 and r < self.size[1] and s  >= 0 and s < self.size[0]:
                    
                    
                    # get the vertex at that position    
                    vertex = self.getVertex(s, r)
                    
                    # if player marked that vertex..
                    if vertex.player == self.Game.currentPlayer():
                        # .. add that vertex to the list
                        Q.append(vertex)
        
        return Q
    
    
    lastMove = None
    def receiveMove(self, move):
        
        
        # first store the last move
        self.lastMove = move
        
        # get the vertex the move pointed on
        vertex = self.getVertex(move[1], move[0])
        
        # mark it
        vertex.player = self.Game.currentPlayer()
        
        # first add it to a new group (later on merge them)
        vertex.group = self._groupCounter
        
        # increment the group counter to avoid conflicts
        self._groupCounter = self._groupCounter +1
        
        # the following lines manipulate the groups of
        # vertices at the border of the gameboard
        # red: left 0, right -1
        # blue: top 0, right -1
        
        if self.Game.currentPlayer() == 1:
            if move[1] == 0:
                vertex.group = 0
            if move[1] == self.size[0]-1:
                vertex.group = -1

        else:
            if move[0] == 0:
                vertex.group = 0
            if move[0] == self.size[1]-1:
                vertex.group = -1
            
        # get the adjacent vertices to that one, which is marked
        adjVertices = self.getSurroundingVertices(move[1], move[0])
        
        # any neightbours?:
        if len(adjVertices) > 0:
            
            # put the marked one to the list
            adjVertices.append(vertex)
            
            # only concentrate on the groups
            groups = [x.group for x in adjVertices]
            
            # WIN Condition
            # either within the gameboard
            # or the last vertex marked has been at the borders
            if (-1 in groups and 0 in groups):
                EventManager.notify("GameFinished")
                
            # get the minimum group
            minGroup = min(groups)
                        
            # set all neighbours to the minimum of the group       
            for key, value in self.Vertices.items():
                if value.group in groups:
                    value.group = minGroup
            
        
    # switch color of all vertices already marked
    def switchColors(self):
        
        # loop for all vertices and invert them
        for key, value in self.Vertices.items():
            
                if value.player == 1:
                    value.player = 2
                elif value.player == 2:
                    value.player = 1
    
    # return last move
    def getLastMove(self):
        return self.lastMove
    
    # game finished event
    def onGameFinished(self):
        self._finished = True
    