import os
from flask import Flask, redirect, url_for, request, render_template, make_response, abort
#from flask import sqlite3
from flask_sqlalchemy import SQLAlchemy

#set projects path, sqlite:/// determines the database engine being used
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = database_file #where database is stored

db = SQLAlchemy(app)
class USER(db.Model): #database of users
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(24))
   pswd = db.Column(db.String(64))
	
   def __repr__(self):
      return "<Name: {}>".format(self.name)
	
	#def __init__(self, name, pswd):
	   #self.name = name
	   #self.name = pswd
error_code = "ERROR"
#~~~DATABASE STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/reg', methods = ['POST', 'GET']) #register
def registration():
   users = None
   if request.form:
      print(request.form);
      user = USER(name = request.form.get("name"))
      db.session.add(user)
      db.session.commit()
      users = USER.query.all() #array of all users usernames
   return render_template("register.html", users = users)
   
   
@app.route('/upd', methods = ['POST', 'GET']) #update
def update():
   newname = request.form.get("newname")
   oldname = request.form.get("oldname")
   user = USER.query.filter_by(name = "fingerguns").first()
   user.name = "banjo"
   print(newname)
   db.session.commit()
   return redirect('/upd')
     
 #~~~SONGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/choose') #pick song
def choose():
   #if request.method == 'POST':
      #song = request.form['sng'] #[] for POST
   if request.method == 'GET':
      song = request.args.get('sng') #() for GET
      
      if song in ['01', '02', '404']:
         return redirect(url_for('get_mic_data',songId = song))
   return render_template('choose_song.html')

@app.route('/microphone/<songId>') #play song
def get_mic_data(songId):
	#return 'Welcome %s' % songId
    return render_template('get_audio.html', sentSongId = songId)
    
	  
#~~~~~CURRENTLY UNUSED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
@app.route('/table')
def table():
   table_values = {'1': 'a', '2': 'b', '3': 'c'}
   return render_template('table.html', result = table_values)
   
@app.route('/loginn',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm'] #[] for POST
      
      if user == 'thom':
         return redirect(url_for('success',name = user))
      else:
         abort(401) #Error 401 - Unauthorised 
	     
   return render_template('login.html')
   
   #if request.method == 'GET':
	  #user = request.args.get('nm') #() for GET
	  #return redirect(url_for('success',name = user))
	  
@app.route('/success/<name>')
def success(name):
   return 'Welcome %s' % name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0", port=5020)
