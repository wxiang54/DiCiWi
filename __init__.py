from flask import Flask, render_template, url_for, redirect, session, request, flash
from pyicloud import PyiCloudService
import util
import solroute

def redirect_url():
    if request.referrer == url_for('appPage'):
        return url_for('index')
    return request.referrer or url_for('index')

app = Flask(__name__)

#Temporary for memories
@app.route('/stuy')
def stuy():
    return render_template("stuy.html")


@app.route('/')
def index():
    try:
        #loggedIn = False
        if ('username' in session) and ('password' in session):
            username = session['username']
            password = session['password']
            verifInt = util.verify(username, password)
            if verifInt == 0: #successful login
                body_title = "Welcome back to SolRoute, %s!" % username
            else:
                alert = "We have detected that you have an invalid session ID. Please login again."
                flash(alert, 'error')
                return render_template("index.html")
        else:
            body_title = "Welcome to SolRoute!"

        return render_template('index.html', body_title=body_title)
    except Exception, e:
        return str(e)


@app.route('/login/', methods=['GET','POST'])
def login():
    try:
        if ('username' in session) and ('password' in session): #already logged in
            alert = "You are already logged in!"
            flash(alert, 'error')
            return redirect( redirect_url() )

        elif request.method == 'GET':
            return render_template('login.html')

        else: #login
            username = request.form.get('username')
            password = request.form.get('password')
            alertList = ["Successfully logged in!", \
                         "Username cannot be left blank!", \
                         "Passwords cannot be left blank!", \
                         "Username does not exist! Please retry or make a new account.", \
                         "Password for %s is incorrect. Please retry or make a new account" % username]

            verifInt = util.verify(username, password)
            if verifInt == 0: #success
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                flash( alertList[0], 'success' )
                return redirect( url_for('index') )
            else:
                flash( alertList[verifInt], 'error' )
                return render_template("login.html")

    except Exception, e:
        return str(e)



@app.route('/register/', methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            if ('username' in session) and ('password' in session): #already logged in
                alert = "You are already logged in!"
                flash(alert, 'error')
                return redirect( redirect_url() )
            else:
                return render_template("register.html")
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            rpassword = request.form.get('rpassword')
            alertList = ["Account Created! You can now log in.", \
                         "Username cannot be left blank!", \
                         "Passwords cannot be left blank!", \
                         "Passwords do not match! Please retry.",\
                         "User %s already exists! If you already have an account, you can log in." % username]
            addUserRet = util.addUser(username, password, rpassword)
            if addUserRet == 0: #success
                flash( alertList[0], 'success' )
                return redirect( url_for('login') )
            else:
                flash(alertList[addUserRet], 'error')
                return render_template("register.html")
    except Exception, e:
        return str(e)


@app.route('/logout/')
def logout():
    try:
        if not ('username' and 'password' in session): #not logged in
            alert = "Not logged in yet!"
            flash( alert, 'error' )
        else:
            session.pop('username', None)
            session.pop('password', None)
            session.pop('appleID', None)
            session.pop('applePass', None)
            session.pop('origin', None)
            session.pop('destin', None)
            session.pop('location', None)
            session.pop('polyline', None)
            alert = "Successfully logged out!"
            flash( alert, 'success' )
        return redirect( redirect_url() )
    except Exception, e:
        return str(e)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/app/', methods=['GET','POST'])
def appPage():
    try:
        if not ('username' and 'password' in session): #not logged in
            alert = "You must be logged in to use this application!"
            flash( alert, 'error' )
            return redirect( redirect_url() )

        if request.method == 'GET':
            if ('appleID' not in session) or ('applePass' not in session):
                return render_template('appleLogin.html')
            if ('origin' not in session) or ('destin' not in session) or ('polyline' not in session):
                return render_template('enterCoords.html')
            return render_template('app.html')

        else:
            if ('appleID' in request.form) or ('applePass' in request.form):
                session.pop('appleID', None)
                session.pop('applePass', None)
                appleID = request.form.get('appleID')
                applePass = request.form.get('applePass')
                try:
                    device = solroute.iCloudLogin(appleID, applePass)
                    flash( 'Successfully logged into iCloud!', 'success' )
                    session['appleID'] = appleID
                    session['applePass'] = applePass
                except:
                    flash( 'Invalid iCloud Credentials!', 'error' )
            elif ('origin' in request.form) or ('destin' in request.form):
                session.pop('origin', None)
                session.pop('destin', None)
                session.pop('polyline', None)
                origin = request.form.get('origin')
                destin = request.form.get('destin')
                #Assume they're good for now
                session['origin'] = origin
                session['destin'] = destin
                session['polyline'] = solroute.getPolyline(origin, destin, "walking", "")
            return redirect( url_for('appPage') )
    except Exception, e:
        return str(e)

# EMBEDDED IN IFRAME IN SOL-ROUTE.COM/APP/
@app.route('/runApp/')
def runApp():
    if ('appleID' not in session) or ('applePass' not in session):
        return "ERROR: Apple ID and password not found in session. Please rerun the application."
    try:
        appleID = session['appleID']
        applePass = session['applePass']
        device = solroute.iCloudLogin(appleID, applePass)
    except:
        return "ERROR: AppleID and ApplePass are incorrect. Please log in again."


    status = device.status()
    name = status.get('name')
    displayName = status.get('deviceDisplayName')
    battery = str( float(status.get('batteryLevel')) * 100 )
    location = solroute.getLocation(device)

    #location = ( "40.6698", "-73.9438" ) #TEMP

    if location is None:
        return "Error: Could not find device location! Make sure the iDevice's location is turned on and reload the application."

    deviceInfo = "%s: %s, %s%% battery remaining" % (name, displayName, battery)
    origin = session.get('origin')
    originCoords = solroute.getCoords(origin)
    destin = session.get('destin')
    destinCoords = solroute.getCoords(destin)
    polyline = util.sanitize(session['polyline'])

    if request.args.get('name') == 'routeInfo':
        template = "routeInfo.html"
    elif request.args.get('name') == 'roadMap':
        template = "roadMap.html"
    else:
        template = "satMap.html"

    return render_template( template,
                            lat=location['latitude'],
                            lng=location['longitude'],
                            deviceInfo=deviceInfo,
                            origin=origin,
                            originCoords=originCoords,
                            destination=destin,
                            destinationCoords=destinCoords,
                            polyline=polyline )

if __name__ == "__main__":
        app.run( debug = True )
