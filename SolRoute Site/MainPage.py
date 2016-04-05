#!/usr/bin/python
print "content-type:text/html\n"
import cgi
import cgitb
import os
if "REMOTE_ADDR" in os.environ:
    ip=os.environ["REMOTE_ADDR"]
else:
    ip=""
cgitb.enable()
form=cgi.FieldStorage()
keys=form.keys()
f=open('loggedin.txt', 'r')
codes=f.read()
codelist=codes.split('\n')
cll=[]
for n in codelist:
    cll.append(n.split(','))
def logcheck():
    for n in cll:
        if n[0]==form.getvalue('user') and str(n[1])==str(form.getvalue('id')) and n[2]==ip:
            return """Please enter your child's starting location and the destination.<br><br><form action="runApp.py"><div id="locationField">
                Starting Point:<br><input id="autocomplete" placeholder="Enter your address" onFocus="geolocate()" type="text" name="start">
                
               <br>
               <br>
                Destination:<br><input id="autocomplete2" placeholder="Enter your address" onFocus="geolocate()" type="text" name="end"></input>
                </div>
                <br>
                <br>
                                <input type="hidden" name="user" value=\""""+ form.getvalue('user')+ """\">
                <input type="hidden" name="id" value=\""""+form.getvalue('id')+"""\">
                    
                <input type="submit" value="Submit">
                </form><br><br>
                <a href=\"logout.py?TheUsername="""+form.getvalue('user')+"&"+"ID="+form.getvalue('id')+"\"> Log Out </a></body>"
    return "You don't seem to be logged in... <br><a href=\"Login.py\"> Login </a>"
	

print """<!DOCTYPE html><html><head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link type="text/css" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500">
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=places"></script>
    <script>
    var autocomplete;
    var autocomplete2;
    function initialize() {
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {HTMLInputElement} */(document.getElementById('autocomplete')));
    autocomplete2 = new google.maps.places.Autocomplete(
    /** @type {HTMLInputElement} */(document.getElementById('autocomplete2')));
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
    });
    google.maps.event.addListener(autocomplete2, 'place_changed', function() {
    });
    }
    </script>
    </head><body onload="initialize()"><img src="drawing.png"><br><br>
    """
print logcheck()
print "</html>"
