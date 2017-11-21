'''
Created on Nov 6, 2017

@author: joely
'''
import json
import requests

i = "hello"
if (i == "hello"):
    print(i)
print("AVLTree is evil")
print("meow meow meow MEOW")

response = requests.get("http://api.open-notify.org/iss-now.json")
print(response.status_code)

response = requests.get("http://api.open-notify.org/iss-pass")
print(response.status_code)

response = requests.get("http://api.open-notify.org/iss-pass.json")
print(response.status_code)


parameters = {"lat": 40.71, "lon": -74}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
print("cool" + response.content)
# these two should give the same thing
response = requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74")
print(response.content)

people = requests.get("http://api.open-notify.org/astros.json")
print(people)
