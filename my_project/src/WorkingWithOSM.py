from osmapi import OsmApi
import overpy
import overpass

MyApi = OsmApi();
print (MyApi.NodeGet(4119542984));
