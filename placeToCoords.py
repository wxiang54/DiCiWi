import requests

'''
Turns Google Maps place_id to a tuple containing place coordinates

Utilizes Google Maps Places API
'''


key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"
placeid = "ChIJN1t_tDeuEmsRUsoyG83frY4"   #SUBJECT TO CHANGE

payload = {'key':key, 'placeid':placeid }
r = requests.get('https://maps.googleapis.com/maps/api/place/details/json?', params=payload)

jsonData = r.json()

coordDict = jsonData["result"]["geometry"]["location"]
coordinates = (coordDict['lat'], coordDict['lng'])