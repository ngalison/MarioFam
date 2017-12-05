from osmapi import OsmApi
import overpy
import overpass


def returnFootpaths(slat, slon, nlat, nlon):
	api = overpy.Overpass()	
	result = api.query("[bbox: " + str(slat) +"," + str(slon) +"," + str(nlat) + "," + str(nlon) +"]; ( node[highway=footway]; node[highway=pedestrian]; node[foot=yes]; node[footway=sidewalk]; way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); out;")
	return len(result.ways)
		
print(returnFootpaths(47.596238,-122.34512, 47.633268, -122.27097))
