from django.shortcuts import render
from django.http import HttpResponse
import requests
import sys
import math
from builtins import str
#from . import point
#from . import boundingbox
#from . import TaskManagerWeb
#from TaskManagerWeb import analyseRegion

clientID = "djgzd3RYazV0V0hGaERkMl9KUGF3UToxYjI4NGMxNTEzMmI2NDVl"

def return_paths(request, xCoord, yCoord, distance):
    xCoord = float(xCoord)
    yCoord = float(yCoord)
    distance = float(distance)
    result = str(xCoord) + ' ' + str(yCoord) + ' ' + str(distance)
    finalCoords = analyseRegion([xCoord, yCoord], distance, 0)
    finalCoordsString = str(finalCoords)
    result += ' ' + finalCoordsString
    html = "<html><body> %s </body></html>" %result
    return HttpResponse(html)


def analyseRegion(coordinates, distance, count):
    bb = BoundingBox.fromPoint(Point.fromList(coordinates), distance)
    requestString = "https://a.mapillary.com/v3/images/?bbox=" + str(bb.lowerx) + "," + str(bb.lowery) + "," + str(bb.upperx) + "," + str(bb.uppery)
    requestString += "&client_id=" + clientID
    boundingbox = requests.get(requestString);
    #Now separate into the list of coordinates
    featureList = boundingbox.json()['features']
    points = []
    for feature in featureList:
        points.append(Point.fromList((feature['geometry']['coordinates'])))

    'Given the points and the bounding box, place each point into the dictionary'
    'For now, use a dictionary with indices 1-9, this is where code to calculate number of subdivisions would go'
    subdivisions = 9
    regionToPoints = data = {k: [] for k in range(1, subdivisions+1)}

    if (not points):
        bb.find_region(Point(bb.lowerx, bb.lowery), subdivisions)
    for point in points:
        mapping = bb.find_region(point, subdivisions)
        regionToPoints[mapping].append(point)

    i = 1
    'User is currently standing in box 5.  We want to check the block directly next to them, meaning boxes 2,4,6,8'
    'for the lowest density'
    minimum = len(regionToPoints[5])
    block = 5
    for k, v in regionToPoints.items():
        if(k % 2 == 0 & len(v) < minimum):
            minimum = len(v)
            block = k
        for point in v:
            #Ensure that the points were properly mapped, can be commented out for better runtime
            assert(point.inBox(bb.indexToBox[k]))
    
    bbCoordinates = bb.indexToBox[block]
    if (count == 2):
        return bbCoordinates

    bbMidX = (bbCoordinates.lowerx + bbCoordinates.upperx) / 2
    bbMidY = (bbCoordinates.lowery + bbCoordinates.uppery) / 2
    if (count != 2):
        count = count + 1
        analyseRegion([bbMidX, bbMidY], distance, count)

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

class Point:
    #Initialize a point directly
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #Initialize with a list
    @classmethod
    def fromList(cls, li):
        return cls(li[0], li[1])
    
    #Returns whether this point is in the specified bounding box.
    def inBox(self, bb):
        return (bb.lowerx <= self.x <= bb.upperx) & (bb.lowery <= self.y <= bb.uppery)
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self):
        return str(self)
