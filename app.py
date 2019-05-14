from flask import Flask, flash, request, redirect, url_for,render_template
from flask_uploads import UploadSet, IMAGES, configure_uploads
from backend import db

app = Flask(__name__)
fileuploads = UploadSet('fileuploads')
configure_uploads(app, fileuploads)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload',methods=["GET",'POST'])
def upload():
    if(request.method=='POST'):
        filename = fileuploads.save(request.form['fileupload'])
        url = fileuploads.url(filename)
        
    else:
        return render_template('upload.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
 
