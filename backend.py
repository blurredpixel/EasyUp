from flask_sqlalchemy import SQLAlchemy
from app import app
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

class Misc():
    genfileid(self):
        return os.urandom(16).hex()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath=db.Column(db.String)
    fileid=db.Column(db.Text)
