
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


@app.route('/login')
# define a method that will execute when we access this end-point
def login_template():
    # flask already knows this templates lives in the templates folder
    return render_template('login.html')


@app.route('/register')
# define a method that will execute when we access this end-point
def register_template():
    # flask already knows this templates lives in the templates folder
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():

    # We get the email and password from the form
    email = request.form['email']
    password = request.form['password']

    # check if the login is valid
    if User.login_valid(email, password):
        User.login(email)
    else:
        # OK, so what happens if we login with a username, it doesn't exist.
        # Turns out we still get that and why?
        # Because the session already exists for this browser, so Google Chrome in my laptop already has the
        # cookie that tells Flask that I'm logged in.
        # So when I access this page, it sees that my username is wrong, but it doesn't do anything.
        # So it still locked me in as the user that was already logged in before.
        # So we want to do is if the user's login is not valid.
        session['email'] = None

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():

    # We get the email and password from the form
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])


if __name__ == "__main__":
    app.run(debug=True)
