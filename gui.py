#These function can be merged into server.py, that way we can jsonify the simple returns 
#from the db and various pools

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
    
@app.route("/")
def hello():
  return render_template('index.html')

if __name__ == "__main__":
  app.debug = True
  app.run()