from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os 


config = {
  "apiKey": "AIzaSyDy556hNFgqo526c0q85OYleiKVlMgp2p0",
  "authDomain": "travelit2023.firebaseapp.com",
  "projectId": "travelit2023",
  "storageBucket": "travelit2023.appspot.com",
  "messagingSenderId": "34652549203",
  "appId": "1:34652549203:web:c507860556a6c26177d6a6",
  "measurementId": "G-SL8X1JWPRC",
  "databaseURL":"https://travelit2023-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def  intro():
    return render_template('intro.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
        # try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        account={"username":username,"full_name":full_name,"email":email,"bio":"","admin":"False"}
        db.child('Users').child(UID).set(account)
        return redirect(url_for('signin'))
        # except:
            # error = "Authentication failed"
    return render_template("signup.html",error=error)
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            UID = login_session['user']['localId']            
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html",error=error)
@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('intro'))
@app.route('/home')
def home():

    return render_template('home.html')
@app.route('/admin',methods=['GET', 'POST'])
def admin():
    try: 
        UID = login_session['user']['localId']
        info=db.child('Users').child(UID).get().val()
    except:
        return redirect(url_for('home'))
    if   info['admin']=='True':     
        if request.method == 'POST' and request.files['photo'] != None:
            country = request.form['country']
            discrption = request.form['discrption']
            links= request.form['links']
            image= request.files['photo']
            filename = image.filename
            UPLOAD_FOLDER = os.path.join('static', 'uploads')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            image_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_filename)
            country={"country":country,"discrption":discrption,"links":links,"photo":image_filename}
            db.child('Countries').push(country)
            return render_template('admin.html')   
        else:
            return render_template('admin.html')
    else:
        return redirect(url_for('home'))
@app.route('/map')
def map():
    countries = db.child('Countries').get().val()
    return render_template('map.html', countries=countries)
@app.route('/allmap')
def allmap():
    countries = db.child('Countries').get().val()
    return render_template('allmap.html', countries=countries)

if __name__ == '__main__':
    app.run(debug=True)