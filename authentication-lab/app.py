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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        username = request.form["username"]
        bio = request.form["bio"]
        #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        user = {'email': email, "password": password, "fullname" : fullname, 'username': username, 'bio': bio}
        db.child("Users").child(UID).set(user)
        return redirect(url_for("add_tweet"))
        #except:
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
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            UID = login_session['user']['localId']
            tweet = {"title": title, "text": text}
            db.child("tweets").push(tweet)
            return redirect(url_for('all_tweets.html'))
        except:
            error = "tweet failed"
            return redirect(url_for('add_tweet'))
    return render_template("add_tweet.html")
@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
    tweets = db.child("tweets").get().val()
    return render_template("all_tweets.html", tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)