from flask import Flask, session, render_template, redirect, url_for, request
import re
import sqlite3 

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)

# login page, we use GET and POST requests
# @app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row 
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password,))
         # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Accessing columns by name instead of by index
            for account in cursor:
                session['loggedin'] == True
                session['id'] == account['id']
                session['username'] == account['username']
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home')) 
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# home page only accessible for loggedin users
@app.route('/home')
def home():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    column=cursor.execute('''SELECT * FROM AUTEURS''')
    rows = cursor.fetchall()
    # alternative use of a list concept
    column = [column[0] for column in column.description]
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', rows=rows, columns=column, username=session['username']) 
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home/questions')
def questions():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    column=cursor.execute('''SELECT * FROM VRAGEN''')
    rows = cursor.fetchall()
    column = [column[0] for column in column.description]
    return render_template('home.html', rows=rows, columns=column)

@app.route('/home/learn_objectives')
def learn_objectives():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    column=cursor.execute('''SELECT * FROM LEERDOELEN''')
    rows = cursor.fetchall()
    column = [column[0] for column in column.description]
    return render_template('home.html', rows=rows, columns=column)

# profile page only accessible for loggedin users
@app.route('/profile')
def profile():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    # Check if user is loggedin
    if 'loggedin' in session:
        # We get all the account info from session for the profile page
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
        # role=session['role'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# logout page
@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()
