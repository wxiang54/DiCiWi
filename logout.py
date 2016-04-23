#!/usr/bin/python
print "content-type:text/html\r\n"
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

print '''
<html>
<head>
<title>Log Out</title>
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
<body>
Successful Logout<br>
<a href="Login.py"> Log Back In </a>
</body>
</html>
'''