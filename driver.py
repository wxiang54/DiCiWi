import math
import requests
from pyicloud import PyiCloudService
from polyline.codec import PolylineCodec

'''
# =============================   I-PHONE   =============================

# Login
appleID = raw_input('Enter your Apple ID: ')
applePass = raw_input('Enter your password: ')

appleData = PyiCloudService(appleID, applePass)

# Choose first device
    # Optional: add fxnality for multiple devices (be able to choose)
device = appleData.devices[0]
#device.play_sound()

print device.location()
# =======================================================================
'''



# ===========================   GOOGLE MAPS   ===========================
key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"
origin = "40.635436,-73.950093"   #(My House)
destination = "40.717946,-74.013905"   #(Stuy)
mode = "walking" #default
avoid = "" #maybe highways

payload = {'origin':origin, 'destination':destination, 'key':key, 'mode':mode, 'avoid':avoid}
r = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=payload)

jsonData = r.json()
route = jsonData["routes"][0]
polyline = route["overview_polyline"]["points"]

# =======================================================================




# ===========================   DATA ANALYSIS   =========================

#This is the list of points from the directions polyline
points = PolylineCodec().decode(polyline)

#This is the list of lines obtained from all the points
lines = []
for i in range(len(points) - 1):
    p1 = points[i]
    p2 = points[i + 1]
    
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    
    #point-slope form of line:   y = mx + b
    if (y2 - y1) == 0:
        m = "undefined" #vertical line
    else:
        m = float(y2 - y1) / float(x2 - x1)   # m = delta y / delta x
    b = y1 - (m * x1) #using 1 point and slope to calculate y-intercept: b = y - mx
    
    lineInfo = {'m':m, 'b':b}
    



# =======================================================================