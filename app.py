from flask import Flask, flash, request, redirect, url_for,render_template
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload',methods=["GET",'POST'])
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
