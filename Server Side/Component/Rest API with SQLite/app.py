from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)



#Model
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    #for relationship use foreign key

    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#Schema(for Serialiser)
class MaterialSchema(ma.Schema):
    class Meta:
        fields = ['name','description','price','qty']

#Init Schema
Material_Schema = MaterialSchema(strict = True)
Materials_Schema = MaterialSchema(many = True, strict = True )

#Create product
@app.route('/material',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_material = Material(name,description,price,qty)

    db.session.add(new_material)
    db.session.commit()

    return Material_Schema.jsonify(new_material)

#Get all materials
@app.route('/material', methods = ['GET'])
def get_materials():
    all_material = Material.query.all()
    result = Materials_Schema.dumps(all_material)

    return jsonify(result.data)

#Get single Material
@app.route('/material/<id>',methods = ['GET'])
def get_material(id):
    material = Material.query.get(id)
    return Material_Schema.jsonify(material)

#Update Material
@app.route('/material/<id>',methods=['PUT'])
def updatematerial(id):
    material = Material.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    material.name = name
    material.description = description
    material.price = price
    material.qty = qty

    db.session.commit()

    return Material_Schema.jsonify(material)

@app.route('/')
def test():
    return jsonify({"msg":"Hello Worlds"})

#Run Server
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) 
