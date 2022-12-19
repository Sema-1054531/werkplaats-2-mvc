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
        # Check if account exists using Sqlite3
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
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM accounts')
    data = cursor.fetchall()
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
         return render_template("home.html", datas=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home/leerdoelen')
def leerdoelen():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM leerdoelen')
    data = cursor.fetchall()
    return render_template("leerdoelen.html", datas=data)

@app.route('/home/vragen')
@app.route('/home/vragen/<int:start>/<int:eind>')
def vragen(start=0, eind=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM vragen")
    columns = [columns[0] for columns in cursor.description]
    rows = cursor.fetchall()
    rows = rows[start:eind]
    return render_template('home.html', rows=rows, columns=columns, pagestart=start, pageend=eind)

@app.route('/home/vragen/opslaan/<question_id>', methods=['POST'])
def opslaan(question_id):
    question_content = request.form["vraag"]
    cursor = connection.cursor()
    cursor.execute("UPDATE vragen SET vraag = '" + question_content + "' where id = " + question_id)
    connection.commit()
    return redirect(url_for("vragen"))

@app.route('/')
@app.route('/filtering/')
def hello_world():
    tables = question_model.get_tables()
    return render_template('list_tables.html', tablenames=tables)

@app.route('/filtering/<table_name>')
def filter_table(table_name):
    columns = question_model.get_columns(table_name)
    return render_template('list_columns.html', columns=columns, table=table_name)

@app.route('/filtering/<table_name>/<column_name>/')
def filter_table_on_column(table_name, column_name):
    datatype = "boolean"
    values = question_model.get_unconvertable_values(table_name, column_name, datatype)
    return render_template("list_unconvertable.html", values=values, table=table_name, column=column_name, datatype=datatype)
# add user
@app.route('/home/add_user', methods=['POST','GET'])
def add_user():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = connection.cursor()
        cursor.execute('INSERT INTO accounts (username, password, email) values (?,?,?)',(username, password, email))
        connection.commit()
        flash('User Added','success')
        return redirect(url_for("add_user"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>",methods=['POST','GET'])
def edit_user(id):
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("update accounts set username=?,password=?,email=? where id=?",(username,password,email,id))
        connection.commit()
        flash('User Updated','success')
        return redirect(url_for("home"))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from accounts where id=?",(id,))
    data = cursor.fetchone()
    return render_template("edit_user.html",datas=data)
    
@app.route("/delete_user/<string:id>",methods=['GET'])
def delete_user(id):
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("delete from accounts where id=?",(id,))
    connection.commit()
    flash('User Deleted','warning')
    return redirect(url_for("home"))

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
