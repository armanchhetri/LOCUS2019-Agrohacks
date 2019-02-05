#importing modules
from model import User, db, app
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

#to add_data

#To update data
@app.route('/dairy/update',methods=["PUT"])
def Dairy_update():
    # if not request.json:
    #     abort(400)
    if 'username' in session:
        username=session['username']
        data=request.json.get()
        user=User.query.filter_by(username=username).first()
        if Dairy.query.filter_by(user=user.id).first():
            dairy=Dairy.query.filter_by(user=user.id).first()
            for i in range(4):
                j=0
                dairy[i].milk=data[i][j]
                j=j+1
                dairy[i].ghee=data[i][j]
                j=j+1
                dairy[i].curd=data[i][j]
                j=j+1
                dairy[i].cheese=data[i][j]
                j=j+1
                dairy[i].bound=data[i][j]
            db.session.commit()
            return jsonify(data)

        else:
            for i in range(4):
                j=0
                milk=data[i][j]
                j=j+1
                ghee=data[i][j]
                j=j+1
                curd=data[i][j]
                j=j+1
                cheese=data[i][j]
                j=j+1
                bound=data[i][j]
                dairy=Dairy("Costraint",milk,ghee,curd,cheese,bound)
                db.session.add(dairy)
            db.session.commit()
            return jsonify(data)





#Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True )
