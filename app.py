from flask import Flask, flash, request, redirect, url_for,render_template
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['UPLOADS_DEFAULT_DEST'] = '/uploads'
fileuploads = UploadSet('fileuploads')

configure_uploads(app, fileuploads)

db = SQLAlchemy(app)

class Misc():
    def genfileid(self):
        return os.urandom(16).hex()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String)
    fileid=db.Column(db.Text)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String)
    password=db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        User(username=request.form['username'],password=)


    return render_template('register.html')

@app.route('/upload',methods=["GET",'POST'])
def upload():
    if(request.method=='POST'):
        filename = fileuploads.save(request.form['fileupload'])
        url = fileuploads.url(filename)
        newfile=File(url=url,fileid=Misc.genfileid())
        db.session.add(newfile)
        db.session.commit()
        
    else:
        return render_template('upload.html')

 
