from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyBzRPe_OMQQU3NNdHMeH7fNUlQl17CKz9k",
  "authDomain": "aloha-d6953.firebaseapp.com",
  "projectId": "aloha-d6953",
  "storageBucket": "aloha-d6953.appspot.com",
  "messagingSenderId": "356364790039",
  "appId": "1:356364790039:web:d0351f44a45368361eaf52",
  "measurementId": "G-CQRZT8NKQ1",
    "databaseURL": "https://aloha-d6953-default-rtdb.europe-west1.firebasedatabase.app/"
}
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
error = ""
db = firebase.database()
user = {}
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        username = request.form["username"]
        bio = request.form["bio "]
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "auth failed :(c"
            return render_template('signup.html')
    return render_template("signup.html")
@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = 'sign in failed'
    return render_template("signin.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

#If the method is 'POST' take the inputs and signin the user with email & password.
#Don't forget to store the user in the login session and to use try and except.
#Redirect the route to the add tweet page


if __name__ == '__main__':
    app.run(debug=True)