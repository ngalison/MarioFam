
#Gets the distance in M between two points in lon and lat
from math import sin, cos, radians, acos, sqrt

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
