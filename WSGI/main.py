#!/usr/bin/python
print "content-type:text/html\n"
import cgi
import cgitb
import os
import time
cgitb.enable()
form=cgi.FieldStorage()


def emoticons(post):
    x = 0
    while x < len(post):
        if post [x]==":" and post[x+1]==")":
            post = post.replace(":","",1).replace(")",'''<img src="smile.jpg" height="21" width="21">''',1)
            x += 1
        if post [x]==":" and post[x+1]=="(":
            post = post.replace(":","",1).replace("(",'''<img src="sad.jpg" height="21" width="24">''',1)
            x += 1
        else:
            x += 1 
    return str(post)


def authenticate():
    if 'user' in form and 'magicnumber' in form:
        #get the data from form, and IP from user.
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        #compare with file
        text = open('loggedin.txt').read().split("\n")
        for line in text:
            line = line.split(",")
            if line[0]==user:#when you find the right user name
                if line[1]==magicnumber and line[2]==IP:
                    return True
                else:
                    return False
        return False#in case user not found
    return False #no/missing fields passed into field storage
#either returns ?user=__&magicnumber=__  or an empty string.

def securefields():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
    return ""

#makes a link, link will include secure features if the user is logged in
def makeLink(page, text):
    return '<a href="'+page+securefields()+'" class="classy">'+text+'</a><br>'
   
if authenticate()==True:
    poster=form.getvalue('user')
    firstpart="<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"login.css\">\n<title>Thread</title>\n</head>\n<body>\n<form>\n<input class=\"myButton\" type=\"text\" name=\"comment\" value=\"Enter comment here\">\n<br><br><input type=\"hidden\" name=\"user\" value=\""+form.getvalue('user')+"\">\n<input type=\"hidden\" name=\"magicnumber\" value=\""+form.getvalue('magicnumber')+"\">\n<input class=\"myButton\" type=\"submit\" value=\"Submit\"></form>\n"
else:
    poster='guest'
    firstpart="<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"login.css\">\n<title>Thread</title>\n</head>\n<body>\n<form>\n<input class=\"myButton\" type=\"text\" name=\"comment\" value=\"Enter comment here\">\n<br><br><input type=\"submit\" value=\"Submit\">\n</form><br>\n"
if 'comment' in form:
    #if "<" in str(emoticons(form.getvalue('comment'))): #tags not allowed otherwise people can manipulate the site
    #    debug= '<br> \n<h2>Plain text only please.</h2>'
    #if "," in str(emoticons(form.getvalue('comment'))): #csv will be messed up
#	debug= '<br> \n<h2>Commas not allowed</h2>!'
    #else:
    comment=form.getvalue('comment')
    comment=comment.replace('<', 'FAILHACK')
    g=open('william sucks at cs.csv', 'a')
    g.write((poster+','+emoticons(comment))+'\n')
    g.close()
else:
    debug=""
f=open('william sucks at cs.csv', 'r')
text=f.read()
text=text.rstrip('\n')
text=text.split('\n')
posts=[]
for n in text:
    posts+=[n.split(',')]
table='<table border=\"1\"><tr><td>User</td><td>Post</td>'
#separates by commas, adds posts to the table
for n in posts:
    table+='\n<tr> <td>  ' + n[0]+'  </td>  <td>'+n[1]+'  </td></tr>'
table+='\n</table>\n</body>\n</html>'
print firstpart+table + "<br>Click" + str(makeLink("page1.py", " here to go home"))