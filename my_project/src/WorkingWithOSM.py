from osmapi import OsmApi
import overpy
import overpass


def returnFootpaths(slat, slon, nlat, nlon):
	api = overpy.Overpass()	
	queryStr = "[bbox: " + str(slat) +"," + str(slon) +"," + str(nlat) + "," + str(nlon) + "]; (way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); out;"
	print (queryStr)
	result = api.query(queryStr)
	return result.ways
		
ways = returnFootpaths(47.596238,-122.34512, 47.633268, -122.27097)
print (ways[0])


