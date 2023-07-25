from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyDy556hNFgqo526c0q85OYleiKVlMgp2p0",
  "authDomain": "travelit2023.firebaseapp.com",
  "projectId": "travelit2023",
  "storageBucket": "travelit2023.appspot.com",
  "messagingSenderId": "34652549203",
  "appId": "1:34652549203:web:c507860556a6c26177d6a6",
  "measurementId": "G-SL8X1JWPRC"
  "databaseURL":"https://travelit2023-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
@app.route('/', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
       try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        account={"username":username,"password":password,"full_name":full_name,"email":email,"bio":""}
        db.child('Users').child(UID).set(account)
        return redirect(url_for('signin'))
       except:
            error = "Authentication failed"
   return render_template("signup.html",error=error)
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
        bio= request.form['bio']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            db.child('Users').child(UID).update(account)["bio"]
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html",error=error)
@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))
@app.route('/home')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)