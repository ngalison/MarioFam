from osmapi import OsmApi
import overpy
import overpass


def returnFootpaths(slat, slon, nlat, nlon):
	api = overpy.Overpass()	
	result = api.query("node(" + str(slat) + "," + str(slon) +"," + str(nlat) + "," + str(nlon) + "); out;")
	##result = api.query("node(47.596238,-122.34512, 47.633268, -122.27097); out;")
	
	return len(result.nodes)
		
print(returnFootpaths(47.596238,-122.34512, 47.633268, -122.27097))


