import numpy as np

class obstacle:
    total = []
    array = []
    
    def __init__(self, x, y, brAngle, is_visible = True):
        self.x = x
        self.y = y
        self.brAngle = brAngle
        self.is_visible = is_visible
        
        obstacle.total.append(self)
        
        if x>0 and x<1:
            obstacle.array.append(self)
  
    def __repr__(self):
        return f"OBSTACLE ({self.x} {self.y}) brAngle={self.brAngle}; is_visible->{self.is_visible}"
    
    @property
    def vector(self):
        return np.array([self.x, self.y])

    def mk_invisible(self):
        self.is_visible = False

