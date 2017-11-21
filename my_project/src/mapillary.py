'''
Created on Nov 21, 2017

@author: alisonng
'''
import requests

boundingbox = requests.get("https://a.mapillary.com/v3/images/?lookat=12.9981086701,55.6075236275&bbox=12.9981086701,55.6075236275,13.0006076843,55.6089295863&client_id=TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2")
print(boundingbox.status_code)

json = boundingbox.json()
print(json)
for el in json['features'] :
    print(el['properties'])