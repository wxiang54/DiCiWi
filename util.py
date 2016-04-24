import hashlib

# Verify a user using users.csv and sha1 encryption
def verify(username, password):
    #0: Success
    #1: Username doesn't exist
    #2: Username exists, but password wrong
    
    userDict = parseUsers()
    if username not in userDict:
        return 1
    if password != (hashlib.sha1(userDict[username]).hexdigest()):
        return 2
    return 0


def addUser(username, password, rpassword):
    #0: Success
    #1: Username field left blank
    #2: One of the password fields left blank
    #3: pass and rpass don't match
    #4: user already exists in users.csv
    
    if username.strip() == "":
        return 1
    if password.strip() == "" or rpassword.strip() == "":
        return 2
    if password != rpassword:
        return 3

    userDict = parseUsers()
    if username in userDict:
        return 4
    
    f=open("/var/www/FlaskApp/solroute/users.csv",'w')
    f.write("%s,%s\n" % (username, password))
    f.close()
    return 0


def parseUsers():
    f=open('/var/www/FlaskApp/solroute/users.csv','r')
    parsedByLine = f.read().split()
    
    d = {}
    for line in parsedByLine:
        userData = line.split(',')
        username = userData[0]
        password = userData[1]
        d[username] = password
    f.close()
    return d








        
