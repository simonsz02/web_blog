
from flask import Flask, render_template, request, session

# object of the Flask class
# __name__ is a built-in variable in python. It contains: "__main__"
from src.common.database import Database
from src.models.user import User

app = Flask(__name__)

# secret key Flask uses to make sure that the data that were sending to user in the form of cookie is secure
app.secret_key = "simon"

# creating the api end-point that are gonna be used
# www.mysite.com/api/


@app.route('/')
# define a method that will execute when we access this end-point
def hello_method():
    # flask already knows this templates lives in the templates folder
    return render_template('login.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    # check if the login is valid
    if User.login_valid(email, password):
        User.login(email)

    return render_template('profile.html', email=session['email'])


if __name__ == "__main__":
    app.run(debug=True)
