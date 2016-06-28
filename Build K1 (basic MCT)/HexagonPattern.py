from tkinter import *

# TODO
# - Subscripts der anderen Klassen benachrichtigen

class HexagonPattern():
    
    
    def __init__(self, HexGUI):
        
        #n=x,m=y
        self.n = HexGUI.Game.size[1]
        self.m= HexGUI.Game.size[0]
        
        self.blue = "#71b6f0"
        self.red = "#d34f4f"
        
        # Sample Hexagon with length of 1
        self.points = [0.866025, 0,
                       1.7320508, 0.5,
                       1.7320508, 1.5,
                       0.866025, 2,
                       0, 1.5,
                       0, 0.5]
        
        self.topMark = [[0, 0.5],
                        [0.866025, 0],
                        [1.7320508, 0.5],
                        [0.866025, 0]]
        
        self.bottomMark = [[0, 0],
                        [0.866025, 0.5],
                        [1.7320508, 0],
                        [0.866025, 0.5]]
                
        self.sideMark = [[0, 0],
                         [0.866025, 0.5],
                         [0.866025, 1.5]]
        
        #self.rightMark = 
        
        # Store basic Game Board class
        self.HexGUI = HexGUI
        
        # Store it's canvas where we're drawing
        self.canvas = HexGUI.canvas
        
        # For design reasons set a margin
        # otherwise it's eye cancer
        self.margin = 40
        self.vergleich=self.n/self.m
        if self.vergleich>=2:
            self.q=self.n + (self.n - 1)/2
            self.scale=(self.HexGUI.canvas_width - 2 * self.margin*self.vergleich) / (self.q*1.7320508)
        else:
            self.q=self.m + (self.m - 1)/2
            self.scale=(self.HexGUI.canvas_width - 2 * self.margin*self.vergleich) / (self.q*1.7320508)
            
        self.spielbrett=[[0,1,0],[2,0,0],[0,0,0]]
            
    
    
    # That cell that's the user hovering above
    ActiveCell = [-1,-1]
    
    # Event Listener
    # Function is called when the user moves over the canvas
    # It subscribes from HexGUI
    def onMouseOver(self, event):
        
        # Determine where the User is pointing at
        Cell = self.mapCoordToCell([event.x,event.y])
        
        # If Cell is within a ceratin range .. 
        if Cell[0] >= 0 and Cell[0] <= self.m and Cell[1] >= 0 and Cell[1] <= self.n:
            
            # .. and the cell is different from the current highlighted
            if Cell != self.ActiveCell:
                
                # store the new highlighted cell
                self.ActiveCell = Cell
                # and redraw the whole scene
                self.draw()
        
    
    
    
    # Convert screen coords to cell coords
    def mapCoordToCell(self, coords):
        
        # Determine the scale of each cell
        
        # Use the inverse functions of those used in the loop later on
        # in the draw function, to get back the i's and j's of the coordinates
        i = round((coords[1] - self.margin) / (1.5 * self.scale) - 0.4330125)
        j = round((((coords[0] - self.margin) / self.scale) - 0.866025 * i) / 1.7320508 -0.4330125)
        
        return [j, i]
        
    # use the sample hexagon and scale it's coordinates
    # and apply a lateral and vertical offset
    def hexagon(self, scale, location = [0, 0]):
        
        L = []
        
        for i, coordinate in enumerate(self.points):
            # x coordinate
            if i % 2 == 0:
                L.append((coordinate * self.scale) + location[0])
            # y coordinate
            else:
                L.append((coordinate * self.scale) + location[1])
        return L
    
    
    def drawMarkings(self):
        L = []
        R = []
        for q in range(self.n):
            for vertex in self.topMark:
                x = vertex[0] * self.scale + self.margin + (q * self.scale * 1.7320508)
                y = vertex[1] * self.scale + self.margin - 2
            
                L.append([x, y])
            
            for vertex in self.bottomMark:
                x = vertex[0] * self.scale + self.margin + (q * self.scale * 1.7320508) + (0.5 * self.m * 1.7320508 * self.scale) - (0.5 * self.scale * 1.7320508)
                y = vertex[1] * self.scale + self.margin + self.m * 1.5 * self.scale + 2
                
                
                R.append([x, y])
        
        R1 = []
        L1 = []
        
        for q in range(self.m):
            for vertex in self.sideMark:
                x = vertex[0] * self.scale + self.margin + (self.n * self.scale * 1.7320508) - (0.5 * 1.7320508 * self.scale) + 2 + (q * self.scale * 1.7320508 * 0.5)
                y = vertex[1] * self.scale + self.margin + (q * 1.5 * self.scale)
                
                v = ((vertex[0] * (-1)) + 0.866025) * self.scale + self.margin - 2 + (q * self.scale * 1.7320508 * 0.5)
                w = ((vertex[1] * (-1)) + 1.5)  * self.scale + self.margin + (q * 1.5 * self.scale) + 0.5 * self.scale
               
                R1.append([x, y])
                L1.append([v, w])
                
        
        for i in range(len(L) -1):
            self.canvas.create_line(L[i][0], L[i][1], L[i+1][0], L[i+1][1], fill=self.blue, width = 5)
        
        L = R
        for i in range(len(L) -1):
            self.canvas.create_line(L[i][0], L[i][1], L[i+1][0], L[i+1][1], fill=self.blue, width = 5)
            
        L = R1
        for i in range(len(L) -1):
            self.canvas.create_line(L[i][0], L[i][1], L[i+1][0], L[i+1][1], fill=self.red, width = 5)
        L = L1
        for i in range(len(L) -1):
            self.canvas.create_line(L[i][0], L[i][1], L[i+1][0], L[i+1][1], fill=self.red, width = 5)
    
    
    # Draws the whole scene using the current state
    # The function has to be called when something changed
    
    
    def draw(self):
        
        
        if self.HexGUI.Game.HexBoard.finished():
            return 0
        
        # Due to the inclination of the board
        # we need got a different projected
        # amount of cells in x direction
        
        self.canvas.delete("all")
        
        # Build the markings
        self.drawMarkings()
        
        
        # main loop to draw the hexagon pattern
        # vertical loop
        for i in range(self.n):
            # horizontal loop
            for j in range(self.m):
                
                # get coords (inverse function used to get back i's and j's in map function)
                x = round((1.7320508 * j + 0.866025 * i) * self.scale) + self.margin;
                y = round(1.5 * i * self.scale) + self.margin
                
                # color to fill the hexagons with
                fillColor = "#ececec"
                
                vertex = self.HexGUI.Game.HexBoard.getVertex(i, j)
                if vertex.player == 1:
                    fillColor= self.blue
                
                if vertex.player == 2:
                    fillColor= self.red
                
                
                # if cell has to be highlighted apply different color
                if self.ActiveCell[0] == j and self.ActiveCell[1] == i:
                    if self.ActiveCell[0] != -1 and self.HexGUI.Game.HexBoard.isMarked(i, j) == False:
                        if self.HexGUI.Game.currentPlayer() == 2:
                            fillColor = self.red
                        else:
                            fillColor = self.blue
                
                
                
                # draw the hexagons
                self.canvas.create_polygon(self.hexagon(self.scale, [x ,y]), outline="#24292e", 
                            fill=fillColor, width=1)
    
        
        