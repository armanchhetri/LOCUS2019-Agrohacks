from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from passlib.apps import custom_app_context as pwd_context

#Configuring Applicaton
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init Database
db = SQLAlchemy(app)
#Init Ma
ma = Marshmallow(app)

#Database Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    contactno = db.Column(db.String(10),nullable = False)
    # location_id = db.Column(db.Integer,db.ForeignKey('districts.id'))
    # location = db.relationship('Districts')
    districtName = db.Column(db.String(15),nullable = False)
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Districts(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(15),nullable = False)


#Marshmallow Serializer
class UserSchema(ma.Schema):
    class Meta:
        fields = ['firstname','lastname','username','email','contactno','districtName']

User_Schema = UserSchema(strict = True)
