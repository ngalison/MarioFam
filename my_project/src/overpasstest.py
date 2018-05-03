import overpy
api = overpy.Overpass()
result = api.query("node(50.745,7.17,50.75,7.18);out;")
len(result.nodes)