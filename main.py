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
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['role'] = account['role']
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            # Redirect to home page for 'editor' or 'admin'
            if session['role'] == 'admin':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# only accessible for admin users
@app.route('/admin_home')
def admin_home():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM accounts")
    result = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM auteurs")
    auteurs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM leerdoelen")
    leerdoelen = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM vragen")
    vragen = cursor.fetchone()[0]
    connection.close()
    # return result
    if session['role'] == 'admin':
         return render_template('admin_home.html', leerdoelen=leerdoelen,auteurs=auteurs,vragen=vragen, result=result, username=session['username'])
    return redirect(url_for('login'))
   
# admin page to manage accounts
@app.route('/admin_home/accounts')
def admin_accounts():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM accounts')
    data = cursor.fetchall()
    if session['role'] == 'admin':
         return render_template('admin_accounts.html', datas=data, username=session['username'])
    return redirect(url_for('login'))

# home page only accessible for loggedin users
@app.route('/home', methods=['GET', 'POST'])
def home():
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if request.method == 'POST':
        dob = request.form['dob']
        if dob == "show-all":
            cursor.execute('SELECT * FROM auteurs')
        elif dob == "1990-1999":
            cursor.execute('SELECT * FROM auteurs WHERE geboortejaar >= 1990 AND geboortejaar <= date("now")')
        else:
            cursor.execute('SELECT * FROM auteurs')
    else:
        cursor.execute('SELECT * FROM auteurs')
    data = cursor.fetchall()
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
         return render_template('home.html', auteurs=data, username=session['username'])
    # User is not loggedin redirect to login page
 
    return redirect(url_for('login'))

# get leerdoelen list
@app.route('/home/leerdoelen')
def leerdoelen():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    connection = sqlite3.connect('./databases/testcorrect_vragen.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM leerdoelen')
    data = cursor.fetchall()
    return render_template("leerdoelen.html", leerdoelen=data)

# zoek de lijst van vragen
@app.route('/home/vragen')
def questions():
    if 'loggedin' not in session:
        return redirect(url_for('login'))    
    cursor = connection.cursor()
    # Initialize an empty list to store the query results
    rows = []
    # Initialize a default value for the dropdown menu
    selected_option = 'all'
    # Check if the dropdown menu has been submitted
    if request.args.get('filter'):
        # Get the selected option from the dropdown menu
        selected_option = request.args.get('filter')
    # If the selected option is 'NULL', only retrieve rows where the leerdoel is NULL
    if selected_option == 'NULL':
        column = cursor.execute('''SELECT * FROM vragen WHERE leerdoel IS NULL''')
        rows = cursor.fetchall()
    # If the selected option is 'br', retrieve rows where the vraag column contains <br> or &nbsp;
    elif selected_option == 'br':
        column = cursor.execute('''SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%' ''')
        rows = cursor.fetchall()
    # If the selected option is 'invalid_leerdoel', retrieve rows where the leerdoel is not in the leerdoelen table
    elif selected_option == 'invalid_leerdoel':
        column = cursor.execute('''SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)''')
        rows = cursor.fetchall()
    # If the selected option is 'all', retrieve all rows
    elif selected_option == 'all':
        column = cursor.execute('''SELECT * FROM vragen''')
        rows = cursor.fetchall()
    # Invalid questions
    invalid_questions_ids = find_invalid_questions()
    invalid_questions_status = {}
    for row in rows:
        if int(row[0]) in invalid_questions_ids:
            invalid_questions_status[row[0]] = True
        else:
            invalid_questions_status[row[0]] = False
    column = [column[0] for column in column.description]
    column.append('action')
    # Check if the download button has been clicked
    if request.args.get('download'):
        # Create a CSV file in memory
        si = StringIO()
        cw = csv.writer(si)
        # Write the column names and rows to the CSV file
        cw.writerow(column)
        cw.writerows(rows)
        # Set the response headers to indicate that the response is a CSV file
        response = make_response(si.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=vragen.csv"
        response.headers["Content-type"] = "text/csv"
        return response
    return render_template('vragen.html', rows=rows, columns=column, invalid_questions_status=invalid_questions_status,  selected_option=selected_option, questions_page=True)

@app.route("/home/ongeldigleerdoel")
def ongeldigleerdoel():
    cursor = connection.cursor()
    column = cursor.execute('''SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)''')
    rows = cursor.fetchall()
    column = [column[0] for column in column.description]
    return render_template('ongeldigleerdoel.html', rows=rows, columns=column)

@app.route("/home/systeemcodes")
def systeemcodes():
    cursor = connection.cursor()
    column = cursor.execute(f"SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%'")
    rows = cursor.fetchall()
    column = [column[0] for column in column.description]
    return render_template('systeemcodes.html', rows=rows, columns=column)

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
        flash(f'Vraag "{id}" is bijgewerkt','success')
        return redirect(url_for('questions', selected_question=id))
        
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
        flash(f'Exceptie "{id}" is bijgewerkt','success')
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
        flash('Gebruiker is bijgewerkt','success')
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
        flash(f'Gebruiker "{username}" is bijgewerkt','success')
        return redirect(url_for("admin_accounts"))
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
        flash(f'Auteur "{voornaam}" is bijgewerkt','success')
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
        flash(f'Leerdoel "{leerdoel}" is bijgewerkt','success')
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
    flash('User is bijgewerkt','warning')
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

# Edit table value function
@app.route('/edit/<table_name>/<column_name>/<id>', methods=['GET', 'POST'])
def edit_table_value(table_name, column_name, id):
    if request.method == 'POST':
        # Get form data
        new_value = request.form['new_value']

        # Update value in database
        cursor = connection.cursor()
        cursor.execute("UPDATE {} SET {} = ? WHERE id = ?".format(table_name, column_name), (new_value, id))
        connection.commit()
        flash(f'Waarde "{id}" is bijgewerkt','success')
        # Redirect to filtered table page
        return redirect(url_for('filter_table_on_column', table_name=table_name, column_name=column_name))

    # Get current value from database
    cursor = connection.cursor()
    cursor.execute("SELECT {} FROM {} WHERE id = ?".format(column_name, table_name), (id,))
    current_value = cursor.fetchone()[0]

    # Render edit form template
    return render_template('edit_form.html', table=table_name, column=column_name, id=id, current_value=current_value)

# edit vragen
@app.route('/home/vragen')
@app.route('/home/vragen/<int:start>/<int:eind>')
def vragen():
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM vragen")
    columns = [columns[0] for columns in cursor.description]
    rows = cursor.fetchall()
    return render_template('vragen.html', rows=rows, columns=columns)

# modal vragen
@app.route('/home/vragen/opslaan/<question_id>', methods=['POST'])
def opslaan(question_id):
    question_content = request.form["vraag"]
    cursor = connection.cursor()
    cursor.execute("UPDATE vragen SET vraag = '" + question_content + "' where id = " + question_id)
    connection.commit()
    return redirect(url_for("vragen"))

# logout page
@app.route('/logout')
def logout():
   # remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('role', None)
   # redirect to login page
   return redirect(url_for('login'))

# run python application
if __name__ == '__main__':
    app.run(debug=True)
    app.run()

