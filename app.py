from flask import Flask, render_template, request
import mysql.connector
from flask_frozen import Freezer
app = Flask(__name__)


try:  
    cnx = mysql.connector.connect(
        user='root',
        password='50Shades@',
        host='127.0.0.1',
        database='computer_store'
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin":
        return render_template("index2.html")

    try:
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))

        user = cursor.fetchone()

        cursor.close()

        if user:
            return render_template("index2.html")
        elif username == "admin" and password == "admin":
            return render_template("index2.html")
        else:
            return "Invalid credentials"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database error"



@app.route('/signup', methods=['POST'])
def signup():
    # Get user input from the form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    try:
        # Connect to the database
        connection = cnx

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Insert user data into the 'users' table (adjust table and column names as needed)
        query1 = "INSERT INTO signup (username, password, email) VALUES (%s, %s, %s)"
        query2 = "INSERT INTO login (username,password) VALUES (%s, %s)"
        cursor.execute(query1, (username, password, email))
        cursor.execute(query2, (username,password))

        # Commit changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Redirect to a success page or login page
        return render_template("index2.html")

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return "Error occurred while signing up"
        



@app.route('/signup')
def signup_():
    return render_template('signup.html')

@app.route('/login')
def login_():
    return render_template('login.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
