from django.shortcuts import render
from django.http import HttpResponse
from . import point
from . import boundingbox
from . import TaskManagerWeb
#from TaskManagerWeb import analyseRegion

def return_paths(request, xCoord, yCoord, distance):
    finalCoords = analyseRegion([xCoord, yCoord], distance, 0)
    finalCoordsString = str(finalCoords)
    html =  "<html><body> %s </body></html>" % finalCoordsString
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

    bbMidX = (bbCoordinates.lowerx + bb.upperx) / 2
    bbMidY = (bbCoordinates.lowery + bb.uppery) / 2
    if (count != 2):
        count = count + 1
        analyseRegion([bbMidX, bbMidY], distance, count)

