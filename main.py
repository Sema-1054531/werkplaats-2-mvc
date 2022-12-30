from flask import Flask, session, render_template, redirect, url_for, request, flash, make_response
import sqlite3
import csv
from io import StringIO

from lib.questionmodel import QuestionModel

app = Flask(__name__)

database_file = "databases/testcorrect_vragen.db"
question_model = QuestionModel(database_file)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)

# login page, we need to use both GET and POST requests
@app.route('/')
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
        # Check if account exists using Sqlite3
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
    cursor.execute('SELECT * FROM accounts')
    data = cursor.fetchall()
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', datas=data,username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# get leerdoelen list
@app.route('/home/leerdoelen')
def leerdoelen():
    if 'loggedin'  not in session:
        return redirect(url_for('login'))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM leerdoelen')
    data = cursor.fetchall()
    return render_template("leerdoelen.html", leerdoelen=data)

# get auteurs list
@app.route('/home/auteurs')
def auteurs():
    if 'loggedin'  not in session:
        return redirect(url_for('login'))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM auteurs')
    data = cursor.fetchall()
    return render_template("auteurs.html", auteurs=data)

# zoek de lijst van vragen
@app.route('/home/vragen')
def questions():
    if 'loggedin'  not in session:
        return redirect(url_for('login'))
    cursor = connection.cursor()
    column = cursor.execute('''SELECT * FROM vragen''')
    rows = cursor.fetchall()
    invalid_questions_ids = find_invalid_questions()
    invalid_questions_status = {}
    for row in rows:
        if int(row[0]) in invalid_questions_ids:
            invalid_questions_status[row[0]] = True
        else:
            invalid_questions_status[row[0]] = False
    column = [column[0] for column in column.description]
    column.append('action')
    return render_template('vragen.html', rows=rows, columns=column, invalid_questions_status=invalid_questions_status, questions_page=True)

# deze functie return de lijst met ids van ongeldige vragen
def find_invalid_questions():
    cursor = connection.cursor()
    invalid_questions_sql = 'SELECT * FROM vragen WHERE ((leerdoel NOT IN (SELECT id FROM leerdoelen)) OR (auteur NOT IN (SELECT id FROM auteurs)) or (vraag LIKE "%<br>%" OR vraag LIKE "%&nbsp%")) and (id not in (SELECT vraag_id from EXCEPTIE_VRAAG))'
    cursor.execute(invalid_questions_sql)
    rows = cursor.fetchall()
    invalid_questions_ids = [row[0] for row in rows]
    return invalid_questions_ids

# zoek de lijst van leerdoelen
def find_learning_objectives():
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM leerdoelen''')
    rows = cursor.fetchall()    
    return rows

# zoek de lijst van auteurs
def find_authors():
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM auteurs''')
    rows = cursor.fetchall()    
    return rows

# edit vraag
@app.route('/home/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    cursor = connection.cursor()
    if 'loggedin'  not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cursor.execute('''SELECT * FROM vragen WHERE id =?''', (id,))
        question = cursor.fetchone()
        if question:
            learning_objectives = find_learning_objectives()
            authors = find_authors()
            return render_template('edit_question.html', question = question, learning_objectives = learning_objectives, authors=authors)
        else:
            return redirect(url_for('home'))
    elif request.method == 'POST':
        question = request.form['question']
        learning_objective = request.form['learning_objective']
        author = request.form['author']
        cursor.execute('''UPDATE vragen SET vraag = ?, leerdoel = ?, auteur = ? WHERE id = ?''', (question, learning_objective, author, id))
        connection.commit()
        flash('Vraag updated','success')
        return redirect(url_for('questions'))

# set vraag als exceptie
@app.route('/home/set_question_as_exception/<int:id>')
def set_question_as_exception(id):
    cursor = connection.cursor()
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    cursor.execute('''SELECT * FROM exceptie_vraag where vraag_id = ?''', (id,))
    exception_question = cursor.fetchone()
    cursor.execute('''SELECT * FROM vragen WHERE id =?''', (id,))
    question = cursor.fetchone()
    if not exception_question and question:
        cursor.execute('''INSERT INTO exceptie_vraag (vraag_id) values(?)''', (id,))
        connection.commit()
        flash('Exceptie updated','success')
    return redirect(url_for('questions'))

# add user
@app.route('/home/add_user', methods=['POST','GET'])
def add_user():
    if 'loggedin'  not in session:
        return redirect(url_for('login'))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = connection.cursor()
        cursor.execute('INSERT INTO accounts (username, password, email) values (?,?,?)',(username, password, email))
        connection.commit()
        flash('Gebruiker Added','success')
        return redirect(url_for("add_user"))
    return render_template("add_user.html")

# edit user
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
        flash('Gebruiker Updated','success')
        return redirect(url_for("home"))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from accounts where id=?",(id,))
    data = cursor.fetchone()
    return render_template("edit_user.html",datas=data)

# edit auteurs
@app.route("/edit_auteurs/<string:id>",methods=['POST','GET'])
def edit_auteurs(id):
    if request.method=='POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        geboortejaar = request.form['geboortejaar']
        medewerker = request.form['medewerker']
        met_pensioen = request.form['met_pensioen']
        connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("update auteurs set voornaam=?,achternaam=?,geboortejaar=?,medewerker=?,met_pensioen=? where id=?",(voornaam,achternaam,geboortejaar,medewerker,met_pensioen,id))
        connection.commit()
        flash('Auteurs Updated','success')
        return redirect(url_for("auteurs"))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from auteurs where id=?",(id,))
    data = cursor.fetchone()
    return render_template("edit_auteurs.html",datas=data)

# edit leerdoelen
@app.route("/edit_leerdoelen/<string:id>",methods=['POST','GET'])
def edit_leerdoelen(id):
    if request.method=='POST':
        leerdoel = request.form['leerdoel']
        connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("update leerdoelen set leerdoel=? where id=?",(leerdoel,id))
        connection.commit()
        flash('Leerdoelen Updated','success')
        return redirect(url_for("leerdoelen"))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from leerdoelen where id=?",(id,))
    data = cursor.fetchone()
    return render_template("edit_leerdoelen.html",datas=data)

# delete user
@app.route("/delete_user/<string:id>",methods=['GET'])
def delete_user(id):
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("delete from accounts where id=?",(id,))
    connection.commit()
    flash('User Deleted','warning')
    return redirect(url_for("home"))

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

@app.route('/display')
def display_rows():
  connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
  cursor = connection.cursor()
  # Select rows where column_name is Null
  cursor.execute("SELECT * FROM vragen WHERE leerdoel IS Null")
  rows = cursor.fetchall()
  connection.close()
  return render_template('display.html', rows=rows)

# get tables
@app.route('/filtering/')
def hello_world():
    tables = question_model.get_tables()
    return render_template('list_tables.html', tablenames=tables)

# get columns
@app.route('/filtering/<table_name>')
def filter_table(table_name):
    columns = question_model.get_columns(table_name)
    return render_template('list_columns.html', columns=columns, table=table_name)

# get uncovertable values
@app.route('/filtering/<table_name>/<column_name>/')
def filter_table_on_column(table_name, column_name):
    datatype = "boolean"
    values = question_model.get_unconvertable_values(table_name, column_name, datatype)
    return render_template("list_unconvertable.html", values=values, table=table_name, column=column_name, datatype=datatype)

# select-table
@app.route('/select-table')
def select_table():
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    cursor.close()

    return render_template('select-table.html', tables=tables)

# display-table
@app.route('/display-table', methods=['POST'])
def display_table():
    # Get the selected table
    table = request.form['table']
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE leerdoel IS NULL")
    rows = cursor.fetchall()
    cursor.execute(f"PRAGMA table_info( {table} )")
    columns = cursor.fetchall()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    cursor.close()

    return render_template('select-table.html', tables=tables, table=table, rows=rows, columns=columns)

@app.route('/download-csv/<table>')
def download_csv(table):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE leerdoel IS NULL")
    rows = cursor.fetchall()
    cursor.execute(f"PRAGMA table_info( {table} )")
    columns = cursor.fetchall()
    cursor.close()

    # Generate CSV data from the table data
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data, quotechar='"')
    csv_writer.writerow([column[1] for column in columns])
    csv_writer.writerows(rows)
    csv_data.seek(0)
    csv_str = csv_data.read()

    # Set the response headers to indicate that the file is a CSV file
    # and prompt the browser to download it
    response = make_response(csv_str)
    response.headers["Content-Disposition"] = f"attachment; filename={table}.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# logout page
@app.route('/logout')
def logout():
   # remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # redirect to login page
   return redirect(url_for('login'))

# run python application
if __name__ == '__main__':
    app.run(debug=True)
    app.run()

# # edit vragen
# @app.route('/home/vragen_update')
# @app.route('/home/vragen_update/<int:start>/<int:eind>')
# def vragen():
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT * FROM vragen")
#     columns = [columns[0] for columns in cursor.description]
#     rows = cursor.fetchall()
#     return render_template('vragen_update.html', rows=rows, columns=columns)

# # modal vragen
# @app.route('/home/vragen_update/opslaan/<question_id>', methods=['POST'])
# def opslaan(question_id):
#     question_content = request.form["vraag"]
#     cursor = connection.cursor()
#     cursor.execute("UPDATE vragen SET vraag = '" + question_content + "' where id = " + question_id)
#     connection.commit()
#     return redirect(url_for("vragen_update"))