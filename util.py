import hashlib
import random

pathToUsers = "/var/www/FlaskApp/solroute/users.csv"

# ============================ SITE LOGIN =============================
def parseUsers():
    '''
    void -> dict
        * dict format: { username1:(password1, salt1),
                         username2:(password2, salt2), ... }

    Helper function to parse users.csv
    '''
    global pathToUsers

    f = open(pathToUsers,'r')
    parsedByLine = f.read().split()

    d = {}
    for line in parsedByLine:
        userData = line.split(',')
        username = userData[0]
        password = userData[1]
        salt = userData[2]
        d[username] = (password, salt)
    f.close()
    return d


def validCreds(username, password):
    '''
    (str, str) -> int

    Checks for valid user-inputed data to
    return a corresponding integer:
        0: Success
        1: Username is blank
        2: password is blank
    Helper function for verify() and addUser()
    '''
    if username.strip() == "":
        return 1
    if password.strip() == "":
        return 2
    return 0


def verify(username, password):
    '''
    (str, str) -> int

    Uses users.csv and SHA-1 encryption/salting to
    return integer corresponding with state:
        0: Success
        1: Username field left blank
        2: Password field left blank
        3: Username doesn't exist
        4: Username exists, but password wrong
    '''
    validInt = validCreds(username, password)
    if validInt != 0:
        return validInt #1 or 2

    userDict = parseUsers()
    if username not in userDict:
        return 3
    salt = userDict[username][1]
    if hashlib.sha1(password + salt).hexdigest() != userDict[username][0]:
        return 4
    return 0


def addUser(username, password, rpassword):
    '''
    (str, str, str) -> int

    Checks for valid user-inputed data to
    return integer corresponding with state:
        0: Success
        1: Username field left blank
        2: One of the password fields left blank
        3: pass and rpass don't match
        4: user already exists in users.csv
    If successful, user data appended to users.csv
    '''
    global pathToUsers

    validInt = validCreds(username, password)
    if validInt == 0:
        validInt = validCreds(username, rpassword)
    if validInt != 0:
        return validInt #1 or 2

    if password != rpassword:
        return 3
    userDict = parseUsers()
    if username in userDict:
        return 4

    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    salt = "".join( random.choice(ALPHABET) for i in range(16) )
    encodedPassword = hashlib.sha1(password + salt).hexdigest()
    f = open(pathToUsers,'a')
    f.write("%s,%s,%s\n" % (username, encodedPassword, salt))
    f.close()
    return 0
# =====================================================================

def sanitize(s):
    retStr = ""
    for i in range(len(s)):
        if s[i] == '\\':
            retStr += "\\\\"
        else:
            retStr += s[i]
    return retStr

# =============================== LOGIN ===============================

# =====================================================================
