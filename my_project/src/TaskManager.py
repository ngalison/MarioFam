'''
Created on Nov 27, 2017

@author: alisonng
'''

import requests
#hardcoded dictionary that contains all of the locations we have as well as the coordinates 
#clientID = "djgzd3RYazV0V0hGaERkMl9KUGF3UToxYjI4NGMxNTEzMmI2NDVl" #ours
clientID = "TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2" #theirs
#clientID = "NzkwYjA2MjI2NGExYjZlODRlMzhiMDdiNzQ5Yjg0ZTU" #our secret

coordinates = {'Drumheller Fountain':[47.653768, -122.307778], 'Mary Gates Hall':[47.655000, -122.308058], 'HUB':[47.655577, -122.305074], 'Red Square':[47.656006, -122.309493], 'Quad':[47.657276, -122.307136], 'IMA':[47.653561595258594, -122.30112433433533], 'Rainier Vista':[47.652243, -122.306728], 'U Village':[47.663177, -122.298192], 'UW Bookstore':[47.660420, -122.312795],'CSE':[47.653444, -122.305999], 'Husky Stadium':[47.650551433765905, -122.30251908302307], 'Burke Museum':[47.660675, -122.310399], 'UW Medical Center':[47.649930, -122.308211], 'West Campus':[47.656094621927, -122.3147714138031], 'North Campus':[47.66022814193434, -122.3051691055298], 'Broken Island':[47.649719, -122.298234] }
print('Listed below are all of the major buildings in the UW area.')
for word in sorted(coordinates.keys()):
    print(word)

userInput = ''    
try:
    userInput = coordinates[input('Enter the building you are closest to: ')]
except KeyError:
    print('Bad Input: Check for spelling or building eligibility')
   
print(userInput)

'Offset is currently set to 0.0029 degrees = 0.2 miles'
offset = 0.0029
lowery = userInput[0] - offset
uppery = userInput[0] + offset
lowerx = userInput[1] - offset
upperx = userInput[1] + offset

requestString = "https://a.mapillary.com/v3/images/?bbox=" + str(lowerx) + "," + str(lowery) + "," + str(upperx) + "," + str(uppery)
requestString += "&client_id=" + clientID
print(requestString)
boundingbox = requests.get(requestString);
print(boundingbox.json())