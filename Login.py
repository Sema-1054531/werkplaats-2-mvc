from flask import Flask, render_template, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')

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



if __name__ == '__main__':
    app.run(debug=True)
