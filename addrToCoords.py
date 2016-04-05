import requests

'''
Turns Google Maps place_id to a tuple containing place coordinates

Utilizes Google Maps Places API
'''


key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"
address1 = "345 Chambers Street, New York, NY, United States"   
address2 = "Stuyvesant High School, New York, NY, United States"


payload1 = {'key':key, 'address':address1}
payload2 = {'key':key, 'address':address2}

r1 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=payload1)
r2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=payload2)

jsonData1 = r1.json()
jsonData2 = r2.json()

coordDict1 = jsonData1["results"][0]["geometry"]["location"]
coordDict2 = jsonData2["results"][0]["geometry"]["location"]

coordinates1 = "%s,%s" % (coordDict1['lat'], coordDict1['lng'])
coordinates2 = "%s,%s" % (coordDict2['lat'], coordDict2['lng'])

print coordinates1
print coordinates2