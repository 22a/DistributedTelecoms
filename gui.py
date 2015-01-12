#These function can be merged into server.py, that way we can jsonify the simple returns 
#from the db and various pools

import webbrowser, os
from flask import Flask, render_template, jsonify
app = Flask(__name__)

bPool = 2000
bPro = 10
wPool = 0
fProg = 0

@app.route('/_return_bPool')
def return_bPool():
  global bPool
  bPool = bPool -1
  return jsonify(result=bPool) #values are hardcoded for display purposes, they will call a function that returns an int size

@app.route('/_return_bPro')
def return_bPro():
  global bPro
  bPro = bPro + 1
  return jsonify(result=bPro)

@app.route('/_return_wPool')
def return_wPool():
  global wPool
  wPool = wPool + 20
  return jsonify(result=wPool)

@app.route('/_return_fProg')
def return_fProg():
  global fProg
  fProg = fProg + 9
  return jsonify(result=fProg%100)

@app.route('/_return_fCread')
def return_fCread():
  ## we should have a var here that is 1 if we're reading in a file, 0 otherwise
  global fProg
  test = 1
  if fProg%90==0:     ##for display purposes hides loading bar every 5 seconds
    test = 0
  return jsonify(result=test)

@app.route('/addWorker')
def return_AddWorker():
  os.system("client.py")
  return
    
@app.route("/")
def hello():
  return render_template('index.html')

if __name__ == "__main__":
  #app.debug = True
  #b = webbrowser.get('firefox')
  #b.open_new('127.0.0.1:5000')      #using webbrowser to automatically open the ui
  webbrowser.open('127.0.0.1:5000')
  app.run()