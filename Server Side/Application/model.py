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
    dairy = db.relationship("Dairy", backref="users")
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

class Dairy(db.Model):
    # __tablename__ = 'dairy'

    id = db.Column(db.Integer, primary_key = True)
    decision_var =db.Column(db.String(32),nullable=False)
    constraint =db.relationship("Constraints",backref="daire")
    # cheese =db.relationship("Constraints",backref="dairy.cheese")
    # curd =db.relationship("Constraints",backref="dairy.curd")
    #available= db.relationship("Constraints",backref="dairy.available")
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __init__(self,decision_var,user):
        self.decision_var=decision_var
        self.user =user



class Constraints(db.Model):
    # __tablename__ = 'constraints'

    id = db.Column(db.Integer, primary_key = True)
    ProCost =db.Column(db.Integer)
    Time =db.Column(db.Integer)
    ManLabour =db.Column(db.Integer)
    demand=db.Column(db.Integer)
    dairy = db.Column(db.Integer, db.ForeignKey("dairy.id"))
    def __init__(self, ProCost,Time,ManLabour,demand,dairy):
        self.ProCost=ProCost
        self.Time= Time
        self.ManLabour=ManLabour
        self.demand=demand
        self.dairy= dairy


class Irrigations(db.Model):
    __tablename__ = 'IrrigationModel'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    water_reserve_effective = db.Column(db.Float)
    water_reserve_maximum = db.Column(db.Float)
    irrigationMax = db.Column(db.Float)
    soil_moisture = db.Column(db.Float)
    rainfall = db.Column(db.Float)

    def needed_water(self):
        pass
    def irrigation_water(self):
        pass
    def __init__(self, water_reserve_effective,water_reserve_maximum,soil_moisture,rainfall,user):
        self.user = user
        self.water_reserve_effective = water_reserve_effective
        self.water_reserve_maximum = water_reserve_maximum
        self.soil_moisture = soil_moisture
        self.rainfall = rainfall
        
