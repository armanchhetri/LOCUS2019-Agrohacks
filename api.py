from flask import Flask, jsonify, make_response,abort,request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
#api = Api(app)

# districts = [
#     {
#         'crop': 'Wheat',
#         'season': 'Summer',
#         'description':'It is grass like crop mainly grown in subtropical regions. Flour of it is used in food'
#     },
#     {
#         'crop': 'Corn',
#         'season': 'winter',
#         'description':'It is tall crop mainly grown in tropical regions. It is used to make popcorns'
#     }
# ]
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error':'पाएन यार'}),404)


@app.route('/agro-hacks/category/districts', methods=['GET'])
def crops_by_district():
    with open("database.json","r") as f:
        data=json.load(f)
    f.close()
    return jsonify({'data':data})
@app.route('/agro-hacks/category/districts/<string:crops>', methods=['GET'])
def get_by_crop(crops):
    with open("database.json","r") as f:
        districts=json.load(f)

    sendcrop=[crop for crop in districts if crop['crop']==crops]
    if len(sendcrop)==0:
        abort(404)
    f.close()
    return jsonify({'crop':sendcrop[0]})
@app.route('/agro-hacks/category/districts', methods=['POST'])
def add_data():
    if not request.json or not 'crop' in request.json:
        abort(400)
    addcrop={
        'crop':request.json['crop'],
        'season':request.json['season'],
        'description':request.json.get('description',"")
        }
    with open("database.json","r") as f:
        districts=json.load(f)

    districts.append(addcrop)
    f.close()
    with open("database.json","w") as f:
        json.dump(districts, f, indent=4)

    f.close()
    return jsonify({'Crops added':addcrop}),201
@app.route('/agro-hacks/category/districts/<string:crops>', methods=['PUT'])
def update(crops):
    with open("database.json","r") as f:
        districts=json.load(f)
    for crop in districts:
         if crop['crop'] == crops:
             ucrop=crop

    f.close()
    if len(ucrop)==0:
        abort(404)
    if not request.json:
        abort(400)
    if 'crop' in request.json and type(request.json['crop']) != str:
        abort(400)
    if 'season' in request.json and type(request.json['season']) != str:
        abort(400)

    if 'description' in request.json and type(request.json['description']) != str:
        abort(400)

    ucrop['crop']=request.json.get('crop', ucrop['crop'])
    ucrop['season']=request.json.get('season', ucrop['season'])
    ucrop['description']=request.json.get('description', ucrop['description'])

    for crop in districts:
         if crop['crop'] == crops:
             crop=ucrop

    with open("database.json","w") as f:
        json.dump(districts, f,indent=4)
    f.close()
    return jsonify({"crops":ucrop})


@app.route('/agro-hacks/category/districts/<string:crops>', methods=['DELETE'])
def delete_crop(crops):
    i=0
    for crop in districts:
        if crop['crop']==crops:
            notthere=False
            break
        else:
            i+=1
            notthere=True
    #dcrop = [crop for crop in districts if crop['crop']==crops]
    if notthere:
        abort(404)

    del districts[i]
    return jsonify({'result':'success'})





if __name__ == '__main__':
    app.run(debug=True )
