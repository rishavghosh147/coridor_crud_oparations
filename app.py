from flask import Flask,request,jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
import json

app=Flask(__name__)

app.config['MONGO_URI']='mongodb://localhost:27017/'
mongo=MongoClient(app.config['MONGO_URI'])
db=mongo.corider # here corider is my database name


@app.route('/users')
def view_users():
    users=db.users.find({})
    temp=[]
    for i,user in enumerate(users):
        temp.append(user)
        temp[i]['_id']=str(temp[i]['_id'])
    return jsonify(temp), 200

@app.route('/users/<id>')
def view_user(id):
    user=db.users.find_one({"_id":ObjectId(id)})
    if user:
        user['_id']=str(user['_id'])
        return jsonify(user), 200
    else: return jsonify({"message":"user does not exist !!!"}), 200

@app.route('/users',methods=['POST'])
def add_user():
    data=json.loads(request.data)
    if len(data)==3 and 'name' in data and 'email' in data and 'password' in data and data['name'] and data['email'] and data['password']: # we can able to reduce this line and output will be same if we use marshmallow
        name=data['name']
        email=data['email']
        password=generate_password_hash(data['password'])
        check=db.users.find_one({"email":email})
        if check is None:
            id=db.users.insert_one({"name":name,"email":email,"password":password})
            return jsonify({"message":"user added successfully."}), 200
        else: return jsonify({"message":"user already exist !!!"}), 400
    return jsonify({"message":"please enter a valid data !!!"}), 403

@app.route('/users/<id>',methods=['PUT'])
def update_user(id):
    data=json.loads(request.data)
    if len(data)==3 and 'name' in data and 'email' in data and 'password' in data:
        password=generate_password_hash(data['password'])
        data['password']=password
        result=db.users.update_one({"_id":ObjectId(id)},{"$set":data})
        return jsonify({"message":"user's data updated successfully."}), 200
    return jsonify({"message":"please enter all three field !!!"}), 400

@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    delete=db.users.delete_one({"_id":ObjectId(id)})
    if delete.acknowledged:
        return jsonify({"message":"user deleted successfully !!!"}), 200
    else: return jsonify({"message":"something went wrong !!!"}), 400