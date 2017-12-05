'''
Created on Dec 4, 2017

@author: Marcus
'''
from builtins import str
class Point:
    #Initialize a point directly
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #Initialize with a list
    @classmethod
    def fromList(cls, li):
        return cls(li[0], li[1])
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self):
        return str(self)