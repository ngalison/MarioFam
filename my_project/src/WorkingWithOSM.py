from osmapi import OsmApi
import overpy
import overpass


def returnFootpaths(slat, slon, nlat, nlon):
	api = overpy.Overpass()	
	result = api.query("way(" + str(slat) +", " + str(slon) + ", " + str(nlat) + ", " + str(nlon) + ");/*added by auto repair*/(._;>;);/*end of auto repair*/out;")
	return result.ways[0]
		
print(returnFootpaths(47.65552266666666, -122.30997633333334, 47.656489333333326, -122.30900966666667))


