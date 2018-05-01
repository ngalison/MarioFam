from osmapi import OsmApi
import overpy
import overpass
from boundingbox import BoundingBox
import random
from ShortDistanceFormula import dist
import sqlite3
from sqlite3 import Error

#given a bounding box and a filename, writes a file of the given filename in GeoJson format with all WAYS with pedestrian tags within the bounding box
def returnFootpathsLineString(bb, filename):
	slat = bb.lowery;
	slon = bb.lowerx;
	nlat = bb.uppery;
	nlon = bb.upperx;
	
	database = "data.db"
	conn = create_connection(database)
	curr = conn.cursor()
	curr.execute("SELECT COUNT(*) FROM paths");
	count = curr.fetchone()[0]
	print("STUFFFF:::" + str(count))

	api = overpy.Overpass()	
	result = api.query(" [bbox: " + str(slat) +", " + str(slon) + ", " + str(nlat) + ", " + str(nlon) + "]; (way[highway=footway]; way[highway=pedestrian]; way[foot=yes]; way[footway=sidewalk] ); /*added by auto repair*/ (._;>;); /*end of auto repair*/ out;")
	tempFootpaths = result.ways
	posFootpaths = []

	#This section is here such that only footpaths of a certain length are returned
	MINPATHLENGTH = 100 # The minimum path length in meters THIS SHOULD BE A PARAMETER PASSED IN

	# Run the length checker on decreasing minpathlength until posFootpaths is not empty
	while not posFootpaths:
		print(MINPATHLENGTH)
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
	
	f = open(filename, "w+")
	
	f.write("{\n")
	
	f.write("\"type\": \"FeatureCollection\",\n")
	f.write("\"features\": [\n")
	wayCount = 0;
	for way in footpaths:
		f.write("{\n")
		f.write("\"type\": \"Feature\",\n")
		f.write("\"geometry\": {\n")
		f.write("\"type\": \"LineString\",\n")
		f.write("\"coordinates\": [")
		nodeCount = 0
		for node in way.nodes:
			f.write("[" + str(node.lon) + "," + str(node.lat) + "]")
			if nodeCount != len(way.nodes) - 1:
				f.write(", ")
			nodeCount = nodeCount + 1
		f.write("]\n")
		f.write("},\n")
		f.write("\"properties\": {}\n")
		if wayCount == len(footpaths) - 1:
			f.write("}\n") #take out last one's comma
		else:
			f.write("},\n")
		f.write("\n")
		wayCount = wayCount + 1
	f.write("]\n")
	f.write("}\n")
		
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None