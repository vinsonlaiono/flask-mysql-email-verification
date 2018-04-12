from flask import Flask, render_template, redirect, request, session, flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'durantula'
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('validationdb')
# now, we may invoke the query_db method
print("all the users", mysql.query_db("SELECT * FROM email;"))

@app.route('/')
def index():

    hello_hash = bcrypt.generate_password_hash('13005907Va')
    print(hello_hash)
    return render_template('index.html')

#
@app.route('/process', methods=['POST', 'GET'])
def process():
    email = request.form['email']

    # checks if email is valid---------------
    if len(email) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    # check is email is aleady in the database------------------
    check = "SELECT email FROM email WHERE email = %(email)s"
    email_stuff =  {'email': email}
    email_check = mysql.query_db(check, email_stuff)
    if email_check:
        flash("Email already exits!")
        return redirect('/')
    # query to insert the email from the user input into the DB----------------
    query = "INSERT INTO email (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
    data = {'email': request.form['email']}
    mysql.query_db(query, data)

    # query for all emails from DB
    all_emails = mysql.query_db("SELECT id, email, created_at FROM email")
    print("Fetched all friends", all_emails)

    return render_template('results.html', email = all_emails, name = email)

@app.route('/results')
def results():
    all_emails = mysql.query_db("SELECT id, email, created_at FROM email")
    return render_template("results.html", email = all_emails)
# -------------DELETE EMAIL----------------
@app.route("/delete/<id>")
def delete(id):
    print(id)
    query = "DELETE FROM email WHERE id = %(id)s;"
    data = {
                'id': id
           }
    mysql.query_db(query, data)

    all_emails = mysql.query_db("SELECT id, email, created_at FROM email")
    # return render_template('results.html', email = all_emails)
    return redirect('/results')

# returns user to main page
@app.route('/go_back')
def goback():
    return redirect('/')



# @app.route('/delete')
# def deleteEmail():
#     deletquery = "DELETE FROM email WHERE id = %()"



if __name__ == "__main__":
    app.run(debug=True)