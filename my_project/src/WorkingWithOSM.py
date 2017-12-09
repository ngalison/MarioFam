from osmapi import OsmApi
import overpy
import overpass


def returnFootpaths(slat, slon, nlat, nlon):
	api = overpy.Overpass()	
	result = api.query(" [bbox: " + str(slat) +", " + str(slon) + ", " + str(nlat) + ", " + str(nlon) + "]; (way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); /*added by auto repair*/ (._;>;); /*end of auto repair*/ out;")
	footpaths = result.ways
	print("{")
	print("\"type\": \"FeatureCollection\",")
	print("\"features\": [")
	count = 0;
	for way in footpaths:
		print("{")
		print("\"type\": \"Feature\",")
		print("\"geometry\": {")
		print("\"type\": \"Point\",")
		print("\"coordinates\": [" + str(way.nodes[0].lon) + ", " + str(way.nodes[0].lat) + "]") #come back to this, not finished
		print("},")
		print("\"properties\": {}")
		if count == len(footpaths) - 1:
			print("}") #take out last one's comma
		else:
			print("},")
		print()
		count = count + 1
	print("]")
	print("}")
		
returnFootpaths(47.65436866666667, -122.30628233333334,47.65678533333334,  -122.30386566666668)


