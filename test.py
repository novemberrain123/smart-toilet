from time import sleep
from flask import Flask, render_template
from flask.helpers import url_for
from main import runMain
app = Flask(__name__)
stop_run = False

count = 0

@app.route('/')
def index():
  return render_template('abc.html')

@app.route('/run/')
def run():
    global stop_run
    while not stop_run:
        sleep(1)
        global count
        count+=1
        return (str(count))

@app.route("/stop/", methods=['GET'])
def set_stop_run():
  global stop_run
  stop_run = True
  return "Application stopped"

if __name__ == '__main__':
  app.run(debug=True)