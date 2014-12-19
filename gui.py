#These function can be merged into server.py, that way we can jsonify the simple returns 
#from the db and various pools

import webbrowser
from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/_return_bPool')
def return_bPool():
  return jsonify(result=4800) #values are hardcoded for display purposes, they will call a function that returns an int size

@app.route('/_return_bPro')
def return_bPro():
  return jsonify(result=15200)

@app.route('/_return_wPool')
def return_wPool():
  return jsonify(result=40)

@app.route('/_return_fProg')
def return_fProg():
  return jsonify(result=90)

@app.route('/_return_fCread')
def return_fCread():
  ## we should have a var here that is 1 if we're reading in a file, 0 otherwise
  return jsonify(result=1)

    
@app.route("/")
def hello():
  return render_template('index.html')

if __name__ == "__main__":
  app.debug = True
  #b = webbrowser.get('firefox')
  #b.open('127.0.0.1:5000')       #using webbrowser to automatically open the ui
  app.run()