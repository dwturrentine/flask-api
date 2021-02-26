import requests

# Base url - location of API - server it's running on
BASE = "http://127.0.0.1:5000/"

"""
Get request to url - CRUD - can pass data in JSON along with url request 
Send information through data - when creating new request
response = requests.put(BASE + "helloworld/daryl", {"name": "daryl"})
"""

response = requests.put(BASE + "helloworld/joe", {"name": "bill", "gender": "male"})

# JSON Gets response information
print(response.json())
input()
response = requests.get(BASE + "helloworld/joe")
print(response.json())