#!/usr/bin/python
print "content-type:text/html\n"
import cgi
import cgitb
cgitb.enable()
form=cgi.FieldStorage()
f=open('loggedin.txt','r+')
sheet=f.read()
user=form.getvalue('TheUsername')
magicNumber=form.getvalue('ID')
def remove(user,magicNumber, sheet):
    p=open('loggedin.txt', 'w')
    ans=[]
    rows=sheet.split('\n')
    for n in rows:
        if not n.split(',')[0]==user:
            ans.append(n)
    final= ""
    for x in ans:
	final+=x+'\n'
    p.write(final)
    p.close()
remove(user, magicNumber, sheet)
f.close()
print 'Successful Logout'
print '<a href="Login.py"> Log Back In </a>'