from functools import wraps

import mysql.connector
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from Chat_Inter_optimisé1 import startChat, getquestion
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration de la connexion MySQL
db_config = {
    'user': 'root',
    #entrer le mdps
    'password': 'root',
    'host': 'localhost',
    'database': 'telecom_assistant',
}

# Connexion à la base de données MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in by verifying if 'user_id' is in session
        if "user_id" not in session:
            # Redirect to the login page if the user is not logged in
            return redirect(url_for("login"))
        # Otherwise, continue with the original route function
        return f(*args, **kwargs)

    return decorated_function


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate form data
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return render_template("register.html", message="All fields are required.")


        # Check if username already exists
        query = '''SELECT * FROM users WHERE username = %s'''
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template("register.html", message="Username already exists. Please choose a different one.")

        # Hash the password
        hashed_password = generate_password_hash(password)
        # Store user data in the database
        query = '''INSERT INTO users (username, password) VALUES (%s, %s)'''
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve user data from the database
        query = '''SELECT * FROM users WHERE username = %s'''
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # Check if username exists and if the password is correct
        if user and check_password_hash(user[2], password):
            # Store user information in the session
            session["user_id"] = user[0]
            session["username"] = user[1]
            # Redirect the user to the home page
            return redirect("/home")
        else:
            return render_template("register.html", message="Invalid username or password.")

    return render_template("register.html")


@app.route('/')
def hello_world():
    return render_template("register.html")


@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect("/home")


@app.route('/home')
@login_required
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
@login_required
def Predict():
    res = getquestion()
    response = jsonify({'result': res})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/chat', methods=['POST'])
@login_required
def Chat():
    data = request.get_json()
    msg = data.get('text', '')
    lang = data.get('lang', '')

    res = startChat(msg, session["user_id"], lang)
    response = jsonify({'result': res, "user": msg})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
