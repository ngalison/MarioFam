'''
Created on Nov 21, 2017

@author: alisonng
'''
import json
import requests

boundingbox = requests.get("https://a.mapillary.com/v3/images/?lookat=12.9981086701,55.6075236275&bbox=12.9981086701,55.6075236275,13.0006076843,55.6089295863&client_id=TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2")
print(boundingbox.status_code)

json = boundingbox.json()
print(json)
for el in json['features'] :
    print(el['properties'])
    
#pseudocode 
#get the data coordinates from the user's cellphone - longitude and latitude 
#create a bounding box from that is 50 meters of all 4 directions of the longitude and latitude 
#call the maillary api to get the information 
#go through each "feature" of the resulting json object.  
#check and see if the data is > 5 years old.  if it is then it's a "bad photo" and treat it like it's
#all bad.
#create some type of density map that would tell us which areas have a low density of photos
#chooses a low density point and returns that location to the user