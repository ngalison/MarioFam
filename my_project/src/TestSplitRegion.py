'''
Created on Dec 4, 2017

@author: Marcus
'''
import math

# Given a bounding box, number of subdivisions, and point, returns the region it would belong to
# Assumes subdivisions is a perfect square.
def find_region(x, y, minx, miny, maxx, maxy, subdivisions):
    numRows = int(math.sqrt(subdivisions))
    deltax = (maxx - minx) / numRows
    deltay = (maxy - miny) / numRows
    
    res = 1
    currx = minx
    curry = miny
    while (currx + deltax < x):
        res += 1
        currx += deltax
    while (curry + deltay < y):
        res += 3
        curry += deltay
    return res

minx = 1.0
miny = 1.0
maxx = 4.0
maxy = 10.0
x = 3
y = 4
subdivisions = 9

print(find_region(x, y, minx, miny, maxx, maxy, subdivisions))
points = [[]]
#point = Point(x, y)

realPoints = [[-122.31192812169945, 47.6614570810238], [-122.31193521966424, 47.66115340231431], [-122.31193522443823, 47.66070126235127], [-122.31193492573357, 47.66014380783554], [-122.31194969832706, 47.659755560834014], [-122.31195494321685, 47.659044323884814], [-122.3141761, 47.66120963], [-122.31343051, 47.66129026], [-122.31276334, 47.66129834], [-122.31194188, 47.66115757], [-122.31196199, 47.66105298], [-122.31195995, 47.66074168], [-122.31195979, 47.65956427], [-122.31198085, 47.65914122]]