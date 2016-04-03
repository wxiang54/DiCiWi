import math
import requests
from pyicloud import PyiCloudService
from polyline.codec import PolylineCodec

def driver():
    device = None #placeholder
        
    #Tuple containing device latitude and longitude
    deviceLocation = iCloudLogin()
    
    key = "AIzaSyASnR1SVRSpja-GdlcSWfZQz51ZeasrurY"
    origin = "40.635436,-73.950093"   #(My House)
    destination = "40.717946,-74.013905"   #(Stuy)
    mode = "walking" #modes include walking, driving, bicycling, and transit
    avoid = "" #maybe highways
    polyline = getPolyline(key, origin, destination, mode, avoid)
    
    
    #List of points obtained from the directions polyline
    points = PolylineCodec().decode(polyline)
    
    
    #List of lines obtained from all the points
    lines = []
    for i in range(len(points) - 1):
        lines.append(pointsToLine( points[i], points[i + 1] ))
    
    
    #Test if mobile device is too far from path
    threshold = .001 #margin of GPS error
    minDistance = threshold + 1 #placeholder value
    for line in lines:
        distDeviceToRoute = distPointToLine(deviceLocation, line)
        if distDeviceToRoute < minDistance:
            minDistance = distDeviceToRoute
            
            
        print "ALERT: iDevice has strayed beyond threshold of path"
        device.play_sound()
        print "ALERT: iDevice has strayed beyond threshold of path"
        
    
    
# =======================================================================

def pointsToLine( point1, point2 ):    
    ''' 
    (list, list) -> dict
    
    points in format: [ <latitude>, <longitude> ]
    line in format: { 'm':<slope>, 'b':<y-intercept> }
    
    Converts 'point1' and 'point2'
    to 'line' in slope-interept form
    '''
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    
    #point-slope form of line:   y = mx + b
    if (x2 - x1) == 0:
        m = "undefined" #vertical line
        b = x1 #no y-intercept -> return x-coord of one point instead (for later calculation)
    else:
        m = float(y2 - y1) / float(x2 - x1)   # m = delta y / delta x
        b = y1 - (m * x1) #using 1 point and slope to calculate y-intercept: b = y - mx
    
    line = {'m':m, 'b':b}
    return line
    
    
def distPointToLine( point, line ):
    '''
    (list, dict) -> float
    
    point in format: [ <latitude>, <longitude> ]
    line in format: { 'm':<slope>, 'b':<y-intercept> }
    
    Converts list 'point' and dict 'line'
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
    
    
def iCloudLogin():
    global device
    '''
    void -> tuple
    
    tuple in format (latitude, longitude)
    
    Utilizes pyicloud module to obtain location of iDevice
    and modify global var 'device'
    
    '''        
    appleID = raw_input('Enter your Apple ID: ')
    applePass = raw_input('Enter your password: ')
    
    appleData = PyiCloudService(appleID, applePass)
    
    # Choose first device
        # Optional: add fxnality for multiple devices (be able to choose)
    device = appleData.devices[0]
    deviceLat = device.location()['latitude']
    deviceLong = device.location()['longitude']
    
    return (deviceLat, deviceLong)
    
    
    
def getPolyline( key, origin, destination, mode, avoid ):
    '''
    (str, str, str, str, str) -> str
    
    Utilizes GoogleMaps Directions API to obtain polyline
    of a path from origin to destination points
    '''
    payload = {'origin':origin, 'destination':destination, 'key':key, 'mode':mode, 'avoid':avoid}
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=payload)
    
    jsonData = r.json()
    route = jsonData["routes"][0]
    polyline = route["overview_polyline"]["points"]
    return polyline
    
# =======================================================================    
    
driver()
    