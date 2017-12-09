from osmapi import OsmApi
import overpy
import overpass
from boundingbox import BoundingBox

def returnFootpaths(bb):
	slat = bb.lowery;
	slon = bb.lowerx;
	nlat = bb.uppery;
	nlon = bb.upperx;
	
	api = overpy.Overpass()	
	result = api.query(" [bbox: " + str(slat) +", " + str(slon) + ", " + str(nlat) + ", " + str(nlon) + "]; (way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); /*added by auto repair*/ (._;>;); /*end of auto repair*/ out;")
	footpaths = result.ways
	
	f = open("geojson.txt", "w+")
	
	f.write("{\n")
	
	f.write("\"type\": \"FeatureCollection\",\n")
	f.write("\"features\": [\n")
	count = 0;
	for way in footpaths:
		f.write("{\n")
		f.write("\"type\": \"Feature\",\n")
		f.write("\"geometry\": {\n")
		f.write("\"type\": \"Point\",\n")
		f.write("\"coordinates\": [" + str(way.nodes[0].lon) + ", " + str(way.nodes[0].lat) + "]\n") #come back to this, not finished
		f.write("},\n")
		f.write("\"properties\": {}\n")
		if count == len(footpaths) - 1:
			f.write("}\n") #take out last one's comma
		else:
			f.write("},\n")
		f.write("\n")
		count = count + 1
	f.write("]\n")
	f.write("}\n")
		
#returnFootpaths(47.65436866666667, -122.30628233333334,47.65678533333334,  -122.30386566666668)
returnFootpaths(BoundingBox(-122.30628233333334, 47.65436866666667, -122.30386566666668, 47.65678533333334))


