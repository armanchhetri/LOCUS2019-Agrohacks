from models import User,app, db
from flask_httpauth import HTTPBasicAuth

from flask import Flask, jsonify, make_response,abort,request,session,url_for
from flask_restful import Resource, Api
from passlib.apps import custom_app_context as pwd_context
# app = Flask(__name__)
auth = HTTPBasicAuth()


# db = SQLAlchemy(app)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    # g.user = user
    return True

@app.route("/home",methods=['GET'])
def home():
    if 'username' in session:
        username=session['username']
        return jsonify({"hello":"You are logged in!"})
    return jsonify('message':"Please login")

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
    return jsonify({ 'username': user.username }), 201



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True )
#for application
