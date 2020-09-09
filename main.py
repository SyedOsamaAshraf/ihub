from flask import Flask,render_template,request,session,redirect,url_for,g,flash
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import datetime

import pandas as pd

import pyrebase
config={
    'apiKey': "AIzaSyB-JADiETlOk_PPFCRdhQdtuuR66GmG6MA",
    'authDomain': "emsfirebaseproject-4a5cf.firebaseapp.com",
    'databaseURL': "https://emsfirebaseproject-4a5cf.firebaseio.com",
    'projectId': "emsfirebaseproject-4a5cf",
    'storageBucket': "emsfirebaseproject-4a5cf.appspot.com",
    'messagingSenderId': "811948832340",
    'appId': "1:811948832340:web:741eb6490f9140aee71fc1"
  }
firebase=pyrebase.initialize_app(config)
storage=firebase.storage()



cred=credentials.Certificate("emsfirebaseproject-4a5cf-firebase-adminsdk-kbdxt-5f8dac7ee4.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
app = Flask(__name__,template_folder='templates', static_folder='static')
app.secret_key='whateveryouwat'

def get_details(user):
	dic=db.collection('employee').document(user).get().to_dict()
	if dic:
		return dic
	return None

def checkouting(email):
	doc=db.collection('Attendance').document(email)
	doc.set({"Checkout-Date-Time":datetime.datetime.now()})

def checkining(email):
	doc=db.collection('Attendance').document(email)
	doc.set({"Checkin-Date-Time":datetime.datetime.now()})

@app.route('/profile',methods=['GET','POST'])
def profile():
	if "data" in session:
		data=session['data']
		return render_template("official.html",data=data)
	return redirect(url_for('login'))

@app.route('/master',methods=['POST','GET'])
def master():
	if "data" in session:
		data=session['data']
		rows=len(data["Project"]["From Date"])
		return render_template("master.html",data=data,rows=rows)
	return redirect(url_for('login'))


@app.route('/container',methods=['POST','GET'])
def container():
	if "data" in session:
		data=session['data']
		rows=len(data["Experience"])
		return render_template("container.html",data=data,rows=rows)
	return redirect(url_for('login'))



@app.route('/checkin',methods=['POST','GET'])
def checkin():
	if "data" in session:
		data=session['data']
		checkining(data['Master Data']['Email'])
		return redirect(url_for('master'))
	return redirect(url_for('login'))


@app.route('/checkout',methods=['POST','GET'])
def checkout():
	if "data" in session:
		data=session['data']
		checkouting(data['Master Data']['Email'])
		return redirect(url_for('master'))
	return redirect(url_for('login'))



@app.route('/upload',methods=['POST','GET'])
def upload():
	if "data" in session:
		data=session['data']
		email=data['Master Data']['Email']
		if request.method == 'POST':
			tenth = request.files['tenth']
			twelveth = request.files['twelveth']
			ug = request.files['ug']
			pg = request.files['pg']
			phd = request.files['phd']
			if tenth:
				file=tenth.filename.split('.')
				storage.child(f"{email}/Certificates/Education/High School.{file[1]}").put(tenth)
			if twelveth:
				file=twelveth.filename.split('.')
				storage.child(f"{email}/Certificates/Education/Inter.{file[1]}").put(twelveth)
			if ug:
				file=ug.filename.split('.')
				storage.child(f"{email}/Certificates/Education/Under Graduate.{file[1]}").put(ug)
			if pg:
				file=pg.filename.split('.')
				storage.child(f"{email}/Certificates/Education/Post Graduate.{file[1]}").put(pg)
			if phd:
				file=phd.filename.split('.')
				storage.child(f"{email}/Certificates/Education/Phd.{file[1]}").put(phd)
			return redirect(url_for('master'))
		return redirect(url_for('master'))
	return redirect(url_for('login'))

@app.route('/uploadex',methods=['POST','GET'])
def uploadex():
	if "data" in session:
		data=session['data']
		email=data['Master Data']['Email']
		if request.method == 'POST':
			offer = request.files['Offer']
			resign = request.files['resign']
			salary = request.files['salary']
			desg = request.files['desg']
			if offer:
				file=offer.filename.split('.')
				storage.child(f"{email}/Certificates/Experience/Offer Letter.{file[1]}").put(offer)
			if resign:
				file=resign.filename.split('.')
				storage.child(f"{email}/Certificates/Experience/Offer Letter.{file[1]}").put(resign)
			if salary:
				file=salary.filename.split('.')
				storage.child(f"{email}/Certificates/Experience/Offer Letter.{file[1]}").put(salary)
			if desg:
				file=desg.filename.split('.')
				storage.child(f"{email}/Certificates/Experience/Offer Letter.{file[1]}").put(desg)
			return redirect(url_for('master'))
		return redirect(url_for('master'))
	return redirect(url_for('login'))




@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='POST':
		user=request.form['user']
		data=get_details(user)
		if data:
			session['data']=data
			return redirect(url_for('profile'))
		return render_template("logging.html")
	return render_template("logging.html")

# @app.before_request
# def before_request():
#   g.user=None
#   if 'data' in session:
#     g.data=session['data']


@app.route('/logout')
def logout():
	try:
		session.pop('data',None)
		return redirect(url_for('login'))
	except:
		return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)