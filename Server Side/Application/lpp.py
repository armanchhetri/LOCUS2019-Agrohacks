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
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    contactno = db.Column(db.String(10),nullable = False)
    # location_id = db.C    olumn(db.Integer,db.ForeignKey('districts.id'))
    # location = db.relationship('Districts')
    districtName = db.Column(db.String(15),nullable = False)
    dairy = db.relationship("Dairy", backref="users")
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Districts(db.Model):
    #__tablename__ = 'districts'
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
    constraints=db.Column(db.String(32),nullable=False)
    milk=db.Column(db.Integer,nullable=False)
    ghee=db.Column(db.Integer,nullable=False)
    curd=db.Column(db.Integer,nullable=False)
    cheese=db.Column(db.Integer,nullable=False)
    # bound=db.Column(db.Integer,nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __init__(self,constraints,milk,ghee,curd,cheese,user):
        self.constraints=constraints
        self.milk=milk
        self.ghee=ghee
        self.curd=curd
        self.cheese=cheese
        # self.bound=bound
        self.user=user


class Irrigations(db.Model):
    #__tablename__ = 'IrrigationModel'
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
    def update(self, water_reserve_effective,water_reserve_maximum,soil_moisture,rainfall):
        self.water_reserve_effective = water_reserve_effective
        self.water_reserve_maximum = water_reserve_maximum
        self.soil_moisture = soil_moisture
        self.rainfall = rainfall


class IrrigationSchema(ma.Schema):
    class Meta:
        fields = ['water_reserve_effective','water_reserve_maximum','soil_moisture','rainfall']

Irrigation_Schema = IrrigationSchema(strict = True)

class Crops(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String(150),nullable = False)
    water_requirement = db.Column(db.Float)
    seedrequirement = db.Column(db.Float)
    humanrequirement = db.Column(db.Integer)
    plantperarea =  db.Column(db.Integer)
    rootdepth_seedling = db.Column(db.Integer)
    rootdepth_vegetative = db.Column(db.Integer)
    rootdepth_flowing = db.Column(db.Integer)

class CropsSchema(ma.Schema):
    class Meta:
        fields = ['Name','water_requirement','seedrequirement','humanrequirement','plantperarea','rootdepth_seedling','rootdepth_vegetative','rootdepth_flowing']

Crops_Schema = CropsSchema(strict = True)
