'''
Created on Dec 4, 2017

@author: Marcus
'''
import math
from . import point
#from point import Point

class BoundingBox:
    # Initialize bounding box directly
    def __init__(self, lowerx, lowery, upperx, uppery):
        self.lowerx = lowerx
        self.lowery = lowery
        self.upperx = upperx
        self.uppery = uppery
        self.indexToBox = {}
        
    #Initialize from a point and distance in miles (calculates bounds based on this)
    @classmethod
    def fromPoint(cls, p, distance):
        offset = 0.00145 * (distance / 0.1)
        lowery = p.y - offset
        uppery = p.y + offset
        lowerx = p.x - offset
        upperx = p.x + offset
        return cls(lowerx, lowery, upperx, uppery)
    
    # Given a bounding box, number of subdivisions, and point p, returns the region it would belong to
    # Assumes subdivisions is a perfect square.
    # Also updates self.indexToBox with a dictionary from index to each sub boundingBox produced by this data.
    def find_region(self, p, subdivisions):
        numRows = int(math.sqrt(subdivisions))
        deltax = (self.upperx - self.lowerx) / numRows
        deltay = (self.uppery - self.lowery) / numRows
        
        self.indexToBox = {}
        currenty = self.lowery
        for i in range(numRows):
            currentx = self.lowerx
            for j in range(numRows):
                self.indexToBox[1 + 3 * i + j] = BoundingBox(currentx, currenty, currentx + deltax, currenty + deltay)
                currentx += deltax
            currenty += deltay
        
        res = 1
        currx = self.lowerx
        curry = self.lowery
        while (currx + deltax < p.x):
            res += 1
            currx += deltax
        while (curry + deltay < p.y):
            res += 3
            curry += deltay
        return res
    
    # Finds the bounding box given a region index, the point and subdivisions
    def get_region_bounds(self, i, p, subdivisions):
        numRows = int(math.sqrt(subdivisions))
        deltax = (self.upperx - self.lowerx) / numRows
        deltay = (self.uppery - self.lowery) / numRows
        
        res = 1
        currx = self.lowerx
        curry = self.lowery
        while (currx + deltax < p.x):
            res += 1
            currx += deltax
        while (curry + deltay < p.y):
            res += 3
            curry += deltay
        
        assert(res == i)
        return BoundingBox(currx, curry, currx + deltax, curry + deltay)
    
    def __str__(self):
        return "([" + str(self.lowerx) + ", " + str(self.lowery) + "],[" + str(self.upperx) + ", " + str(self.uppery) + "])"
    
    def __repr__(self):
        return str(self)
        
