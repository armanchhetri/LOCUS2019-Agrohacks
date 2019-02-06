#importing modules
from model import User, db, app, Irrigations, Irrigation_Schema, Dairy
from flask_httpauth import HTTPBasicAuth
from flask import Flask, jsonify, make_response,abort,request,session,url_for
from passlib.apps import custom_app_context as pwd_context
from lpp import IrrigationOptimize, solve_dairy

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
        return jsonify({"status":True})
    else:
        return jsonify({"status":False})

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

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('home'))


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

#To update data
@app.route('/dairy/update/<id>',methods=["PUT"])
def Dairy_update(id):
    # if not request.json:
    #     abort(400)
    if 'username' in session:
        username=session['username']
        data=request.json
        # user=User.query.filter_by(id=id).first()
        if Dairy.query.filter_by(user=id).first():
            dairy=Dairy.query.filter_by(user=id)
            for i in range(3):
                j=0
                dairy[i].milk=data[i][j]
                j=j+1
                dairy[i].ghee=data[i][j]
                j=j+1
                dairy[i].curd=data[i][j]
                j=j+1
                dairy[i].cheese=data[i][j]

            db.session.commit()
            return jsonify(data)

        else:
            for i in range(3):
                j=0
                milk=data[i][j]
                j=j+1
                ghee=data[i][j]
                j=j+1
                curd=data[i][j]
                j=j+1
                cheese=data[i][j]
                #j=j+1
                #bound=data[i][j]
                dairy=Dairy("Costraint",milk,ghee,curd,cheese,id)
                db.session.add(dairy)

            db.session.commit()
            return jsonify(data)

        return jsonify({"message":"login please"})

#Implement
@app.route('/dairy/solve/<id>',methods=['POST'])
def solve(id):
    data=request.json
    if "profit" in data:
        profit=Dairy("profit",data["profit"][0],data["profit"][1],data["profit"][2],data["profit"][3],id)
        db.session.add(profit)
        db.session.commit()
    bound=data["bound"]
    result=solve_dairy(id, bound)
    return jsonify(result)


#For Creating User Irrigation databases
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

#Calculation of Irrigation Problem
@app.route('/user/irrigation/calculation/<id>', methods = ['POST'])
def irrigationOpti(id):
    crops = request.json.get('crops')
    areas = request.json.get('Area')
    drainage = request.json.get('Drainage')
    Irrigation = Irrigations.query.filter_by(user = id).first()
    data =  {
        'crops':crops,
        'Area':areas,
        'ResW':Irrigation.water_reserve_effective,
        'RainW':Irrigation.rainfall,
        'RainWM':Irrigation.rainfall,
        'SM':Irrigation.soil_moisture,
        'DW':drainage,
        'NW':[40,400],
        'ResWM':600,
        'IW':15000
    }
    result = IrrigationOptimize(data)
    return jsonify(result)

#Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="0.0.0.0",port="8000" )
