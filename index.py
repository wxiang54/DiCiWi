#!/usr/bin/python
print "content-type:text/html\r\n"
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
            return """
<form action="runApp.py">
	<h3> iCloud Credentials: </h3>
	
	<input type="text" name="appleID" placeholder="Apple ID"></input> <br>
	<input type="password" name="applePass" placeholder="Password"></input> 
	
	<br><br><br>



	<h3>Please enter your child's starting location and the destination:</h3>
	<div id="locationField">
               &nbsp;<input id="autocomplete" placeholder="Start location" onFocus="geolocate()" type="text" name="start">
               <br>
		<br>
               <input id="autocomplete2" placeholder="End Location" onFocus="geolocate()" type="text" name="end"></input>
                </div>
                <br>
                <br>
                <input type="hidden" name="user" value=\""""+ form.getvalue('user')+ """\">
                <input type="hidden" name="id" value=\""""+form.getvalue('id')+"""\">
                    
                <input type="submit" value="Submit">
                </form>
		<br>
		NOTE: Our program will automatically choose the shortest path from start to end.
		<br><br><br><br>
                <a href=\"logout.py?TheUsername="""+form.getvalue('user')+"&"+"ID="+form.getvalue('id')+"\"> Log Out </a></body>"
    return "You don't seem to be logged in... <br><a href=\"Login.py\"> Login </a>"
	

print """<!DOCTYPE html><html><head>

    <title>SolRoute: Travel Safely</title>

<link rel="shortcut icon" href="http://www.sol-route.com/favycon.ico" type="image/x-icon">
<link rel="icon" href="sol-route.com/favycon.ico" type="image/x-icon">



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

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-76223201-1', 'auto');
  ga('send', 'pageview');

</script>


    </head><body onload="initialize()"><img src="drawing.png"><br><br>
    """
print logcheck()
print "</html>"
