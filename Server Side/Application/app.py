#importing modules
from model import User, db, app, Irrigations, Irrigation_Schema, Dairy
from flask_httpauth import HTTPBasicAuth
from flask import Flask, jsonify, make_response,abort,request,session,url_for
from passlib.apps import custom_app_context as pwd_context

#Init App and Auth
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'ManishBhai'
app.config['SESSION_TYPE'] = 'memcached'


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return True

@app.route("/home",methods=['GET'])
def home():
    if 'username' in session:
        username=session['username']
        return jsonify({"Username":username})
    else:
        return jsonify({'message':"Please login"})

@app.route("/login", methods=['POST'])
def login():
    username=request.json.get('username')
    password=request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments

    if verify_password(username, password):
        session['username']=username
        return jsonify({'username':username})

    return jsonify({'message':"Invalid Details"})

@app.route('/sign-up', methods = ['POST'])
def new_user():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    contactno=request.json.get('contactno')
    username = request.json.get('username')
    password = request.json.get('password')
    districtName = request.json.get('districtname')
    if username is None or password is None or firstname is None or email is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(firstname=firstname,lastname=lastname,email=email,contactno=contactno,districtName=districtName,username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username,'firstname':user.firstname,'lastname':user.lastname,'contact':user.contactno,'email':user.email,'id':user.id }), 201

#For updating User 
@app.route('/user/<id>',methods = ['PUT'])
def modify_user(id):
    user = User.query.get(id)
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    contactno = request.json.get('contactno')
    districtName = request.json.get('districtname')
    
    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.contactno = contactno
    user.districtName = districtName
    db.session.commit()
    return jsonify({ 'username': user.username,'firstname':user.firstname,'lastname':user.lastname,'contact':user.contactno,'email':user.email }), 201

#for creating User Databases
@app.route('/user/irrigation/<id>', methods = ['POST'])
def create_irrigation(id):
    user = request.json.get('id')
    water_reserve_effective = request.json.get('EffectiveWaterReserve')
    water_reserve_maximum = request.json.get('MaximumWaterReserve')
    soil_moisture = request.json.get('SoilMoisture')
    rainfall = request.json.get('Rainfall')
    irrigation = Irrigations(water_reserve_effective, water_reserve_maximum, soil_moisture, rainfall, id)
    db.session.add(irrigation)
    db.session.commit()

    return Irrigation_Schema.jsonify(irrigation)

    
#for Updating User Databases
@app.route('/user/irrigation/<id>', methods = ['PUT'])
def update_irrigation(id):
    irrigation = Irrigations.query.filter_by(user = id).first()
    water_reserve_effective = request.json.get('EffectiveWaterReserve')
    water_reserve_maximum = request.json.get('MaximumWaterReserve')
    soil_moisture = request.json.get('SoilMoisture')
    rainfall = request.json.get('Rainfall')
    irrigation.water_reserve_effective = water_reserve_effective
    irrigation.water_reserve_maximum = water_reserve_maximum
    irrigation.soil_moisture = soil_moisture
    irrigation.rainfall = rainfall
    #irrigation.update(water_reserve_effective, water_reserve_maximum, soil_moisture, rainfall)
    db.session.commit()
    return Irrigation_Schema.jsonify(irrigation)

#Run Server
if __name__ == '__main__':
    app.run(debug=True )
