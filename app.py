from flask import Flask, flash, request, redirect, url_for,render_template,session
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
app.secret_key=os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
fileuploads = UploadSet('fileuploads')

configure_uploads(app, fileuploads)

db = SQLAlchemy(app)

class Misc():
    randint=os.urandom(16).hex()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String)
    fileid=db.Column(db.Text)
    filename=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String)
    password_hash=db.Column(db.Text)
    files= db.relationship('File', backref='User',lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file/<userid>')
def file(userid):
    print('userid: {}'.format(userid))
    print('sessionuserid: {}'.format(session['username']))
    if(str(userid) == str(session['username'])):
        files=File.query.filter_by(user_id=User.query.filter_by(username=session['username']).first().id).all()
    
        return render_template('file.html',username=session['username'],files=files)
    else:
        return redirect('/')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        session['username']=request.form['username']
        u=User(username=request.form['username'])
        session['userid']=u.id
        u.set_password(request.form['password'])
        db.session.add(u)
        db.session.commit()
        return redirect('/upload')
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
       u = User.query.filter_by(username=request.form['username']).first()
       session['userid']=u.id
     
       if u.check_password(request.form['password']):
           session['username']=request.form['username']
           url = 'file/'+str(u.username)
           return redirect(url)
       else:
           flash('Login issue',category="error")
           return render_template('login.html')
    return render_template('login.html')



@app.route('/upload',methods=["GET",'POST'])
def upload():
    if(request.method=='POST'):
        filename = fileuploads.save(request.files['fileupload'])
        print(filename)
        url = fileuploads.url(filename)
        print('FileURL: {}'.format(url))
        fileid=Misc().randint #generates random fileid
        session['fileid']=fileid

        u = User.query.filter_by(username=session['username']).first() #generates user object
        
        newfile=File(filename=filename,url=url,fileid=fileid,user_id=session['userid'])
        u.files.append(newfile) #append new upload file to user modeel of files
        db.session.add(newfile) #add the file to db transactions
        db.session.commit() #commit the transaction
        url = 'file/'+str(session['username'])
        return redirect(url)
        
    else:
        return render_template('upload.html')

 
