from Pattern import *

class SamplePattern(Pattern):
    
    def __init__(self, ki):
        super().__init__(ki)
        
        self.name = "SamplePattern"
        
        
        # 1 opponent
        # 2 self
        # 0 not marked
        # -0/-1/-2 not neccessarily given
        
        self.Sample = """  -1 0 1
                            -2 0 ?
                            -1 1 ?"""
        
        # x flip, y flip, x+y flip, rotation 90, roation -90
        self.Flags = "110"
        
        self.Strategy = """ ? ? ?
                            ? 1 ?
                            ? ? ?"""
    
    def init(self):
        
        if self.Flags[0] == "1":
            
            print("Flipping x")
        
        if self.Flags[1] == "1":
            
            print("Flipping y")
        
        if self.Flags[2] == "1":
            
            print("Flipping x+y")
        
        if self.Flags[3] == "1":
            
            print("Rotating 90")
        
        if self.Flags[4] == "1":
            
            print("Rotating -90")
    
    def calc(self):
        
        # slicing
        
        # matching
        
        
        return 0