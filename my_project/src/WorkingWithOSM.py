from osmapi import OsmApi
import overpy
import overpass

OSMapi = OsmApi();
OVERPASSapi = overpy.Overpass();
#print (MyApi.NodeGet(4119542984));
points = OVERPASSapi.query("node(50.745,7.17,50.75,7.18);out;")
print(len(points.nodes))
