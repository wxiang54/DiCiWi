from polyline.codec import PolylineCodec
from pyicloud import PyiCloudService
import requests
import time
import math
import util

key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"

def driver(appleID, applePass, originAddr, destAddr, device):
    origin = getCoords(originAddr)
    dest = getCoords(destAddr)
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


# ========================== COORDINATE PROCESSING ==========================
def pointsToLine( point1, point2 ):
    '''
    (tuple, tuple) -> dict
        * point tuples format: ( <latitude>, <longitude> )
        * line dict format: { 'm':<slope>, 'b':<y-intercept> }

    Converts tuples 'point1' and 'point2'
    to 'line' dict in slope-interept form
    '''
    x1 = float(point1[0])
    x2 = float(point2[0])
    y1 = float(point1[1])
    y2 = float(point2[1])

    #point-slope form of line: y = mx + b
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
        * point tuple format: ( <latitude>, <longitude> )

    Converts tuples 'point1' and 'point2' to a float 'distance'
    from one point to the other using Cartesian distance formula
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
        * point tuple format: ( <latitude>, <longitude> )
        * line dict format: { 'm':<slope>, 'b':<y-intercept> }

    Converts tuple 'point' and dict 'line' to a float 'distance' from
    the point to the line using point-to-distance formula
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
# ===========================================================================


# ================================ iCLOUD ===============================
def iCloudLogin(appleID, applePass):
    '''
    str, str -> str

    Utilizes pyicloud module to validate iCloud account
    and return first device found on account (assume iPhone)
    '''
    appleData = PyiCloudService(appleID, applePass)

    # Choose first device
    # Optional: add fxnality for multiple devices (be able to choose)
    device = appleData.devices[0]
    return device


def getLocation(device):
    '''
    void -> tuple

    Utilizes pyicloud module to return location of iDevice
    '''
    return device.location()
    deviceLat = device.location()['latitude']
    deviceLong = device.location()['longitude']
    location = (deviceLat, deviceLong)
    return location
# =======================================================================



# =============================== GOOGLE MAPS ===============================
def getCoords( address ):
    '''
    (str, str) -> str
        * Output string in form: "<latitude>,<longitude>"

    Utilizes GoogleMaps Geocoding API to return string of coordinates
    '''
    global key
    payload = {'key':key, 'address':address}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=payload, verify=False)
    json = r.json()
    coordDict = json["results"][0]["geometry"]["location"]
    return "%s,%s" % (coordDict['lat'], coordDict['lng'])

def getPolyline( originAddr, destAddr, mode, avoid ):
    '''
    (str, str, str, str) -> str

    Utilizes GoogleMaps Directions API to obtain a polyline
    representation of path from origin to destination
    '''
    global key
    origin = getCoords(originAddr)
    destination = getCoords(destAddr)
    payload = {'origin':origin, 'destination':destination, 'key':key, 'mode':mode, 'avoid':avoid}
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=payload, verify=False)

    jsonData = r.json()
    route = jsonData["routes"][0]
    polyline = route["overview_polyline"]["points"]
    return polyline

# ===========================================================================


#driver(appleID, applePass, originAddr, destAddr)
