#! /usr/bin/python
print "content-type:text/html\r\n"
import cgi
import cgitb
import os
import requests
import math, requests, time
from pyicloud import PyiCloudService
from polyline.codec import PolylineCodec

device = None #placeholder, updates after iCloudLogin()
location = (0,0) #placeholder, updates after updateLocation()


def driver(appleID, applePass, originAddr, destAddr):
    
    iCloudLogin(appleID, applePass)
    
	
    key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"

    origin = getCoords(key, originAddr)
    dest = getCoords(key, destAddr)

    mode = "walking" #modes include walking, driving, bicycling, and transit
    avoid = "" #maybe highways
    polyline = getPolyline(key, origin, dest, mode, avoid)
    
   	  
    #List of points obtained from the directions polyline
    points = PolylineCodec().decode(polyline)
    
    
    #List of lines obtained from all the points
    lines = []
    for i in range(len(points) - 1):
        lines.append(pointsToLine( points[i], points[i + 1] ))
        
    
    #Test if mobile device is too far from path
    threshold = .001 #margin of GPS error

    
    # =======================================================================
    atDestination = False
        
    while not(atDestination):
        updateLocation()
        minDistance = threshold + 1 #placeholder value, reset minDistance
        
        #update minDistance
        for line in lines:
            distDeviceToRoute = distPointToLine(location, line)
            if distDeviceToRoute < minDistance:
                minDistance = distDeviceToRoute
                
        if distPointToPoint(location, dest) < threshold:
            atDestination = True
            break
        elif minDistance > threshold:
            #device.play_sound()
            print "ALERT: iDevice has strayed beyond threshold of path"
            time.sleep(1)
    # =======================================================================


# =======================================================================

def pointsToLine( point1, point2 ):
    '''
        (tuple, tuple) -> dict
        
        points in format: ( <latitude>, <longitude> )
        line in format: { 'm':<slope>, 'b':<y-intercept> }
        
        Converts tuples 'point1' and 'point2'
        to 'line' in slope-interept form
        '''
    x1 = float(point1[0])
    x2 = float(point2[0])
    y1 = float(point1[1])
    y2 = float(point2[1])
    
    #point-slope form of line:   y = mx + b
    if (x2 - x1) == 0:
        m = "undefined" #vertical line
        b = x1 #no y-intercept -> return x-coord of one point instead (for later calculation)
    else:
        m = float(y2 - y1) / float(x2 - x1)   # m = delta y / delta x
        b = y1 - (m * x1) #using 1 point and slope to calculate y-intercept: b = y - mx
        
    line = {'m':m, 'b':b}
    return line


def distPointToPoint( point1, point2 ):
    '''
        (tuple, tuple) -> float
        
        points in format: ( <latitude>, <longitude> )
        
        Converts tuples 'point1' and 'point2'
        to a float 'distance' from one point to the other
        Utilizes Cartesian distance formula
        '''
    x1 = float(point1[0]) #point x coord
    x2 = float(point1[1]) #point y coord
    y1 = float(point2[0]) #slope of line
    y2 = float(point2[1]) #y-intercept of line
    
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


def distPointToLine( point, line ):
    '''
        (tuple, dict) -> float
        
        point in format: ( <latitude>, <longitude> )
        line in format: { 'm':<slope>, 'b':<y-intercept> }
        
        Converts ltuple 'point' and dict 'line'
        to a float 'distance' from the point to the line
        Utilizes point-to-distance formula
        '''
    x = point[0] #point x coord
    y = point[1] #point y coord
    m = line['m'] #slope of line
    b = line['b'] #y-intercept of line
    
    
    if type(m) != float:
        #distance is horizontal distance from point to vertical line
        distance = abs(y - b)
        return distance
    
    distance = abs((m * x) + b - y) / math.sqrt(1 + (m ** 2))
    return distance


def iCloudLogin(username, password):
    global device
    '''
        void -> void
        
        Utilizes pyicloud module to log access iCloud data on iDevice
        and update global var 'device'
        '''
    
    appleID = username
    applePass = password
    appleData = PyiCloudService(appleID, applePass)
    
    # Choose first device
    # Optional: add fxnality for multiple devices (be able to choose)
    device = appleData.devices[0]


def updateLocation():
    global device, location
    '''
        object -> void
        
        Utilizes pyicloud module to update location of iDevice
        '''
    deviceLat = device.location()['latitude']
    deviceLong = device.location()['longitude']
    location =  (deviceLat, deviceLong)


def getCoords( key, address ):
    '''
    (str, str) -> str
        
    Utilizes GoogleMaps Geocoding API to obtain string of coordinates 

    Output string in form: "<latitude>,<longitude>"
    '''

    payload = {'key':key, 'address':originAddr}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=payload, verify=False)

    json = r.json()
    coordDict = json["results"][0]["geometry"]["location"]

    return "%s,%s" % (coordDict['lat'], coordDict['lng'])


def getPolyline( key, origin, destination, mode, avoid ):
    '''
        (str, str, str, str, str) -> str
        
        Utilizes GoogleMaps Directions API to obtain polyline
        of a path from origin to destination points
        '''
    payload = {'origin':origin, 'destination':destination, 'key':key, 'mode':mode, 'avoid':avoid}
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=payload, verify=False)
    
    jsonData = r.json()
    route = jsonData["routes"][0]
    polyline = route["overview_polyline"]["points"]
    return polyline

# =======================================================================



print """
<!DOCTYPE html>
<html>
<head>    <link rel="stylesheet" type="text/css" href="style.css">

<title>Progress:</title>

<link rel="shortcut icon" href="http://www.sol-route.com/favycon.ico" type="image/x-icon">
<link rel="icon" href="sol-route.com/favycon.ico" type="image/x-icon">

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-76223201-1', 'auto');
  ga('send', 'pageview');

</script>
</head>
<body><br>
<h1>Running application...</h1>
<img src="http://tk20.com/img/webinars/loading-circles.gif">

"""

cgitb.enable()
form=cgi.FieldStorage()
keys=form.keys()

appleID = form.getvalue("appleID")
applePass = form.getvalue("applePass")
originAddr = form.getvalue("start")
destAddr = form.getvalue("end")



print """
</body>
</html>
"""

#driver(appleID, applePass, originAddr, destAddr)