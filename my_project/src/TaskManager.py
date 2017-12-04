'''
Created on Nov 27, 2017

@author: alisonng
'''

import requests

#hardcoded dictionary that contains all of the locations we have as well as the coordinates 
clientID = "djgzd3RYazV0V0hGaERkMl9KUGF3UToxYjI4NGMxNTEzMmI2NDVl" #ours
#clientID = "TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2" #theirs
#clientID = "NzkwYjA2MjI2NGExYjZlODRlMzhiMDdiNzQ5Yjg0ZTU" #our secret

coordinates = {'Drumheller Fountain':[-122.307778 ,47.653768], 'Mary Gates Hall':[-122.308058,47.655000], 'HUB':[-122.305074, 47.655577], 'Red Square':[-122.309493, 47.656006], 'Quad':[-122.307136,47.657276], 'IMA':[-122.30112433433533,47.653561595258594], 'Rainier Vista':[-122.306728, 47.652243], 'U Village':[ -122.298192,47.663177], 'UW Bookstore':[-122.312795,47.660420],'CSE':[-122.305999,47.653444], 'Husky Stadium':[-122.30251908302307,47.650551433765905], 'Burke Museum':[-122.310399,47.660675], 'UW Medical Center':[-122.308211,47.649930], 'West Campus':[-122.3147714138031,47.656094621927], 'North Campus':[-122.3051691055298,47.66022814193434], 'Broken Island':[-122.298234,47.649719] }
print('Listed below are all of the major buildings in the UW area.')
for word in sorted(coordinates.keys()):
    print(word)

userInput = '' 
distance = 0.0000
while(len(userInput) == 0):
    try:
        userInput = coordinates[input('Enter the building you are closest to: ')]
    except KeyError:
            print('Bad Input: Check for spelling or building eligibility')

while(distance == 0):
    try:
            distance = float(input('How far are you willing to walk in terms of miles? Just enter the number. (ex: 0.1, 1.0. 2.0): '))
    except ValueError:
        print('Bad Input: Enter a numeric value')
   
print(userInput)

offset = 0.00145 * (distance / 0.1)
lowery = userInput[1] - offset
uppery = userInput[1] + offset
lowerx = userInput[0] - offset
upperx = userInput[0] + offset

requestString = "https://a.mapillary.com/v3/images/?bbox=" + str(lowerx) + "," + str(lowery) + "," + str(upperx) + "," + str(uppery)
requestString += "&client_id=" + clientID
print(requestString)
boundingbox = requests.get(requestString);
print(boundingbox.json())

'Now separate into the list of coordinates'
featureList = boundingbox.json()['features']
points = []
for feature in featureList:
    points.append(feature['geometry']['coordinates'])
    
print("Found " + str(len(points)) + " points: " + str(points))