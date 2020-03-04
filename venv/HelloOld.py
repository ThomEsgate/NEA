from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

error_code = "ERROR"

@app.route('/success/<name>')
def success(name):
   return 'Welcome %s' % name

@app.route('/')
def index():
      return render_template("index.html")

@app.route('/table')
def table():
   table_values = {'1': 'a', '2': 'b', '3': 'c'}
   return render_template('table.html', result = table_values)

@app.route('/login/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm'] #[] for POST
      return redirect(url_for('success',name = user))
      
   return render_template('login.html')
   
   if request.method == 'GET':
	  user = request.args.get('nm') #() for GET
	  return redirect(url_for('success',name = user))

@app.route('/microphone')
def get_mic_data():
   return render_template("get_audioOld.html")
   
   
if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0", port=5020)

#https://www.tutorialspoint.com/flask/flask_http_methods.htm
#I was here 16/01 - 12:40
