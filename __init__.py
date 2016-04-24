from flask import Flask, render_template, url_for, redirect, session, request
from util import *

app = Flask(__name__)

@app.route('/')
def index():
    '''
    if 'username' and 'password' in session:
        username = session['username']
        password = session['password']
        verifInt = verify(username, password)
        msg = "Welcome back to SolRoute, %s" % username
    else:
        msg = "Welcome to SolRoute!"

    return render_template('index.html', msg=msg)
    '''
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    '''
    if request.method == 'GET':
        return render_template('login.html')
        
    elif 'username' and 'password' in session: #already logged in
        msg = "You're already logged in!"
        return redirect( url_for(index), msg=msg )

    elif request.form[mode] == 'signup'
        msgList = ["Account Created! You can now log in."]
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
        
        addUserRet = addUser(username, password, rpassword)
        verifInt = verify(username, password)
        

    else: #login
        verifInt = verify(username, password)
        session['username'] = request.form['username']
        session['password'] = request.form['password']
    

    '''
    return "login"


@app.route('/logout')
def logout():
    #return redirect(url_for('index'))
    return "logout"


if __name__ == "__main__":
    app.run( debug = True )
