from flask import Flask, render_template
from flask.helpers import url_for
from main import runMain
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/run/')
def run():
    return runMain()

if __name__ == '__main__':
  app.run(debug=True)