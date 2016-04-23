#!/usr/bin/python
print "content-type:text/html\r\n"
import cgi
import cgitb
import string
import md5
import os
import random
if "REMOTE_ADDR" in os.environ:
    ip=os.environ["REMOTE_ADDR"]
else:
    ip=""
m = md5.new()

cgitb.enable()
workingpassword=""
html="""
<!DOCTYPE html>
<html>

<head>
<link rel="shortcut icon" href="http://www.sol-route.com/favycon.ico" type="image/x-icon">
<link rel="icon" href="sol-route.com/favycon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="style.css">
    <title> Log In
    </title>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-76223201-1', 'auto');
  ga('send', 'pageview');

</script>
</head>

<body><img src="drawing.png">
    <br>"""

html2=""" 
<form action="Login.py" method="GET">
    <table>
        <th colspan="2"> Create An Account </th>
        <tr>
            <td>Username</td>
            <td><input type="text" name="Username"> </td>
        </tr>
        <br>
        <tr>
            <td>Select a Password:</td>
            <td><input type="password" name="Password"> </td>
        </tr>
        <br>
        <tr>
            <td>Confirm Password:</td>
            <td><input type="password" name="Confirmation"> </td>
        </tr>
        <br>
        <tr>
            <td>Submit:</td>
            <td><input type="submit" name="Submit" value="Submit"></td>
        </tr>
        <table>
</form>
    """
form=cgi.FieldStorage()
keys=form.keys()
f=open('Passwords.txt', 'r')
text=f.read()
def create(text):
    hasPunctuation=0
    punctuation=set(string.punctuation)
    punctuation.update(['<','>','&lt', '&rt'])
    if 'Username' in form and 'Password' in form:
        list=text.split(',')
        x=0
        while x<len(list):
            if form.getvalue('Username').lower()==list[x]:
                return "Registration Failed: Username Already Taken, Please Try Again "
            x+=1
        for c in punctuation:
            if c in form.getvalue('Username'):
                return 'Registration Failed: INVALID USERNAME Please use only letters and numbers.'
                hasPunctuation=1
        if '<' in form.getvalue('Password') or '>' in form.getvalue('Password'):
            return 'Registration Failed. Do not use special symbols.'
        if len(form.getvalue('Password'))<6 or len(form.getvalue('Password'))>24:
            return 'Registration Failed: Password length must be between 6 and 24!'
        elif form.getvalue('Password')==form.getvalue('Confirmation'):
            m.update(form.getvalue('Password'))
            hashedPassword=m.hexdigest()
            text+=form.getvalue('Username').lower()+','+hashedPassword+','
            w=open('Passwords.txt', 'w')
            w.write(text)
            w.close()
            return "Registration Complete!"
        else:
            return "Registration Failed: Passwords do not match, please type password twice carefully "
    else:
        return ""

g=open('loggedin.txt', 'r')
users=g.read()
assignedid=str(random.randint(0,99999))


def loggedin(users):
    users+=form.getvalue('TheUsername')+','+assignedid+','+str(ip)+'\n'
    p=open('loggedin.txt', 'w')
    p.write(users)
    p.close()
g.close()

def authenticate(text):
    uplist=text.split(',')
    x=0
    while x<len(uplist):
        if uplist[x]==form.getvalue('TheUsername').lower():
            m.update(form.getvalue('ThePassword'))
            hashedPassword=m.hexdigest()
            if uplist[x+1]==hashedPassword:
                loggedin(users)
                return "<a href=\"http://sol-route.com/?user="+form.getvalue("TheUsername")+"&id="+assignedid+"\">MainPage</a> To use SolRoute, you need a mobile device with tracking. Solroute is currently optimized for the following: iPhone</p>"
            else:
                return 'Login Failed: Password Incorrect. Please Try Again.'
        x+=2
    return 'Login Failed: Username not found. Try registering a new account with that username.'






html3=""" <table>
    <th colspan="2"> Log In with Existing Account </th>
    <form action="Login.py" method="GET">
    <tr> <td> Enter Username:</td> <td> <input type="text" name="TheUsername"> </td> </tr>
    <br>
    <tr> <td> Enter Password:</td> <td> <input type="password" name="ThePassword"> </td> </tr>
    <br>
    <tr> <td> Log In:</td> <td> <input type="submit" name="Login" value="Login\"> </td> </tr> </table>"""

q=open('Passwords.txt', 'r')
newtext=q.read()

if form.getvalue('Submit')=='Submit':
    print html+create(text)+html2+html3+'</body>\n</html>'
elif form.getvalue('Login')=='Login':
    print html+html2+authenticate(newtext)+html3+'</body>\n</html>'
else:
    print html+html2+html3+'</body>\n</html>'


