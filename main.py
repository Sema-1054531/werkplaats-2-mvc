from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3 

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)

# login page, we need to use both GET and POST requests
# @app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
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
                assert session['loggedin'] == True
                assert session['id'] == account['id']
                assert session['username'] == account['username']
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
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username']) 
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home/auteurs')
def auteurs():
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM auteurs")
    columns = [columns[0] for columns in cursor.description]        
    rows = cursor.fetchall()
    return render_template('home.html', rows=rows, columns=columns)

@app.route('/home/vragen')
def vragen():
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM vragen")
    columns = [columns[0] for columns in cursor.description]
    rows = cursor.fetchall()
    return render_template('home.html', rows=rows, columns=columns)

@app.route('/home/leerdoelen')
def leerdoelen(): 
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM leerdoelen")
    columns = [columns[0] for columns in cursor.description]
    rows = cursor.fetchall()
    return render_template('home.html', rows=rows, columns=columns)

# profile pageonly accessible for loggedin users
@app.route('/profile')
def profile():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row 
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account) 
        # this can be used to assign privileges 
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
