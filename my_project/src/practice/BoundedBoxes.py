import requests

clientID = "djgzd3RYazV0V0hGaERkMl9KUGF3UToxYjI4NGMxNTEzMmI2NDVl"



def getBoundedBox(lowerx, lowery, upperx, uppery, points):
	requestString = "https://a.mapillary.com/v3/images/?bbox=" + str(lowerx) + "," + str(lowery) + "," + str(upperx) + "," + str(uppery)
	requestString += "&client_id=" + clientID
	boundingbox = requests.get(requestString);
	featureList = boundingbox.json()['features']
	for feature in featureList:
  	 	 points.append(feature['geometry']['coordinates'])

allUWPoints = []
getBoundedBox(-122.32186317443848, 47.647205000176236, -122.29585647583006, 47.66504053437091, allUWPoints)
print (str(allUWPoints))
