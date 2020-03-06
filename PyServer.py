import os
from flask import Flask, redirect, url_for, request, render_template, make_response, abort
#from flask import sqlite3
from flask_sqlalchemy import SQLAlchemy

#~~~DATABASE STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#set projects path, sqlite:/// determines the database engine being used
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = database_file #where database is stored

db = SQLAlchemy(app)

class USER(db.Model): #database of users
   #id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
   name = db.Column(db.String(24), primary_key = True)
   pswd = db.Column(db.String(64))
	
   def __repr__(self): #for representing user as a string
      return "<Name: {}>".format(self.name)
	
   #def __init__(self, name, pswd):
      #self.name = name
      #self.name = pswd
	   
error_code = "ERROR"   #from werkzeug generate_password_hash, check_password_hash https://stackoverflow.com/questions/32493631/unboundlocalerror-local-variable-cursor-referenced-before-assignment

@app.route("/reg", methods=["GET", "POST"])
def register():
   if request.form:
      user = USER(name = request.form.get("name")) #https://stackoverflow.com/questions/32493631/unboundlocalerror-local-variable-cursor-referenced-before-assignment
      db.session.add(user)
      db.session.commit()
   users = USER.query.all()
   return render_template("register.html", users = users)

@app.route("/upd", methods=["GET", "POST"]) #WOOOOOORKKK
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    print(newname)
    print(oldname)
    user = USER.query.filter_by(name = oldname).first()
    user.name = newname
    db.session.commit()
    return redirect("/reg")


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
