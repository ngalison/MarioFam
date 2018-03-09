#This program uses the Haversine formula to find the distance between two 
#long/lat points. Is really only accurate on big distances
#So this is probably not what we will use for the final proj
from math import sin, cos, sqrt, atan2, radians

#Gets the distance in km between two points in lon and lat
def getDistanceFromLonLatInKm(lat1, lon1, lat2, lon2):
    R = 6371.81 #The radius of the earth in KM
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = sin(dLat/2)**2.0 + cos(lat1) * cos(lat2) * sin(dLon/2)**2.0
    c = 2.0 * atan2(sqrt(a), sqrt(1.0-a))
    d = R * c
    return d
