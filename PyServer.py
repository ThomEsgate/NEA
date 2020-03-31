import os
from flask import Flask, redirect, url_for, request, render_template, make_response, abort
#from flask import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

#~~~DATABASE STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#set projects path, sqlite:/// determines the database engine being used
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = database_file #where database is stored

db = SQLAlchemy(app)

class USER(db.Model): #database of users
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(24))
   #pswd = db.Column(db.String(64))
   usersongs = db.relationship('SONGUSER', backref = 'owner')
   
   def __repr__(self): #for representing user as a string
      return "<Name: {}>".format(self.name)   

class SONGUSER(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   owner_id = db.Column(db.Integer, db.ForeignKey(USER.id))
   #songuserArray = db.Column(ARRAY(db.String(24), dimensions = 2), db.ForeignKey('song.SongArray'))

class SONG(db.Model): #database of songs
   songId = db.Column(db.Integer, primary_key = True)
   #songArray = db.Column(ARRAY(db.String(32), dimensions = 2))
   

   
#from werkzeug generate_password_hash, check_password_hash https://stackoverflow.com/questions/32493631/unboundlocalerror-local-variable-cursor-referenced-before-assignment
@app.route("/")
def index():
	 return redirect("/choose")

@app.route("/reg", methods=["GET", "POST"])
def register():
   books = None
   if request.form:
      try:
         user = USER(name = request.form.get("name")) #https://stackoverflow.com/questions/32493631/unboundlocalerror-local-variable-cursor-referenced-before-assignment
         db.session.add(user)
         db.session.commit()
         
      except Exception as exptn:
         print("~~~ERROR ADDING USER~~~")
         print(exptn)
         
   users = USER.query.all()
   return render_template("register.html", users = users)

@app.route("/upd", methods=["GET", "POST"]) #WOOOOOORKKK
def update():
   try:
      newname = request.form.get("newname")
      oldname = request.form.get("oldname")
      user = USER.query.filter_by(name = oldname).first()
      user.name = newname
      db.session.commit()
      
   except Exception as exptn:
      print("~~~ERROR UPDATING USER DETAILS~~~")
      print(exptn)
      
   return redirect("/reg")
@app.route("/del", methods = ["POST"])
def delete():
   name = request.form.get("name")
   user = USER.query.filter_by(name = name).first() 
   print(user)
   db.session.delete(user)
   db.session.commit()
   return redirect("/reg")

 #~~~SONGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
errorcode = ""
@app.route('/choose') #pick song
def choose():
   #if request.method == 'POST':
      #song = request.form['sng'] #[] for POST
   if request.method == 'GET':
      song = request.args.get('sng') #() for GET
      mode = request.args.get('mde')
      
      if song in ['01', '02', '03', '404'] and mode in ['C', 'Eb']:
         redirect(url_for('get_mic_data',songId = song, modeId = mode))
         
   return render_template('choose_song.html', error_code = errorcode)
   
@app.route('/microphone/<songId>/<modeId>') #play song
def get_mic_data(songId, modeId):
	#return 'Welcome %s' % songId
    print(song)
    print(mode)
    return render_template('get_audio.html', sentSongId = songId, sentMode = modeId)
    
	  
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
