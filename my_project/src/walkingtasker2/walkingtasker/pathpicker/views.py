from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import sys
import math
from math import sin, cos, radians, acos, sqrt
from builtins import str
from osmapi import OsmApi
import overpy
import overpass
import random
import json

clientID = "djgzd3RYazV0V0hGaERkMl9KUGF3UToxYjI4NGMxNTEzMmI2NDVl"

def dist(lat1, lon1, lat2, lon2):
    #Uses Equirectangular approx
    R = 6378137 #The radius of the radius of the earth in km
    lat1 = radians(lat1) #fi1
    lat2 = radians(lat2) #fi2
    lon1 = radians(lon1) #lambda1
    lon2 = radians(lon2) #lambda2
    df = lat2 - lat1 #Delta fi
    dd = lon2 - lon1 #Delta lambda
    x = dd * cos((lat1 + lat2)/2)
    y = df
    d = sqrt(x*x + y*y) * R
    return d

def return_paths(request, xCoord, yCoord, distance):
    xCoord = float(xCoord)
    yCoord = float(yCoord)
    distance = float(distance)
    #these coordinates represent the Quad, using them for testing that algorithm is working same as TaskManager.py
    #xCoord = -122.307136
    #yCoord = 47.65776
    #distance = .2
    finalCoords = analyseRegion([xCoord, yCoord], distance, 0)
    #finalCoordsString = str(finalCoords)
    #result = 'This is the bounding box that will be passed into WorkingWithOSM: ' + finalCoordsString
    result = printFootpathsLineString(finalCoords)
    resultJson = json.loads(result)
    return JsonResponse(resultJson)
    #html = "<html><body> %s </body></html>" %result
    #return HttpResponse(html)


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
        bbCoordinates = analyseRegion([bbMidX, bbMidY], distance, count)
    return bbCoordinates

def printFootpathsLineString(bb):
    slat = bb.lowery;
    slon = bb.lowerx;
    nlat = bb.uppery;
    nlon = bb.upperx;
    api = overpy.Overpass()	
    result = api.query(" [bbox: " + str(slat) +", " + str(slon) + ", " + str(nlat) + ", " + str(nlon) + "]; (way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); /*added by auto repair*/ (._;>;); /*end of auto repair*/ out;")
    tempFootpaths = result.ways
    
    # tempTempFootpaths = [];
    # for way in tempFootpaths:
    #     if len(way.nodes)> 4:
    #         tempTempFootpaths.append(way)

    posFootpaths = []

    #This section is here such that only footpaths of a certain length are returned
    MINPATHLENGTH = 250 # The minimum path length in meters

    # Run the length checker on decreasing minpathlength until posFootpaths is not empty
    while not posFootpaths:
        for way in tempFootpaths:
            length = len(way.nodes)
            nodes = way.nodes
            firstNode = nodes[0]
            lastNode = nodes[length - 1]
            lat1 = firstNode.lat
            lon1 = firstNode.lon
            lat2 = lastNode.lat
            lon2 = lastNode.lon
            distance = dist(lat1, lon1, lat2, lon2)
            if distance >= MINPATHLENGTH:
                posFootpaths.append(way)
        if not posFootpaths:
            MINPATHLENGTH = MINPATHLENGTH / 2 

    randomSelection = random.choice(posFootpaths)
    footpaths = [randomSelection]
    result = "{\n"
    result += "\"type\": \"FeatureCollection\",\n"
    result += "\"features\": [\n"
    count = 0
    for way in footpaths:
        result += "{\n"
        result += "\"type\": \"Feature\",\n"
        result += "\"geometry\": {\n"
        result += "\"type\": \"LineString\",\n"
        result += "\"coordinates\": ["
        nodeCount = 0
        for node in way.nodes:
            result += "[" + str(node.lat) + "," + str(node.lon) + "]"
            if nodeCount != len(way.nodes) - 1:
                result += ", "
            nodeCount = nodeCount + 1
        result += "]\n"
        result += "},\n"
        result += "\"properties\": {}\n"
        if count == len(footpaths) - 1:
            result += "}\n" #take out last one's comma
        else:
            result += "},\n"
        result += "\n"
        count = count + 1
    result += "]\n"
    result += "}\n"
    return result

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

