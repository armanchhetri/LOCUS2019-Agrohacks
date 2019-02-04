# from models import db, User
from flask_httpauth import HTTPBasicAuth

from flask import Flask, jsonify, make_response,abort,request
from flask_restful import Resource, Api

app = Flask(__name__)
auth = HTTPBasicAuth()



from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    # g.user = user
    return True

@app.route("/api/resource",methods=['GET'])
@auth.login_required
def resource():
    return jsonify({"hello":"hello you are logged in!"})


@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    # if User.query.filter_by(username = username).first() is not None:
    #     abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True )
