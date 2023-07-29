from flask import Blueprint, json, jsonify, request
from flask_restful import Resource,Api
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from database import db

user=Blueprint("user",__name__,url_prefix="/users") 
api=Api(user)

class User(Resource):
    def get(self,id):
        user=db.users.find_one({"_id":ObjectId(id)})
        if user:
            user['_id']=str(user['_id'])
            return set_http_status_code(user,200)
        else: return set_http_status_code({"message":"user does not exist !!!"},200)

    def put(self,id):
        data=json.loads(request.data)
        if len(data)==3 and 'name' in data and 'email' in data and 'password' in data:
            password=generate_password_hash(data['password'])
            data['password']=password
            result=db.users.update_one({"_id":ObjectId(id)},{"$set":data})
            return set_http_status_code({"message":"user's data updated successfully."},200)
        return set_http_status_code({"message":"please enter all three field !!!"},400)

    def delete(self,id):
        delete=db.users.delete_one({"_id":ObjectId(id)})
        if delete.acknowledged:
            return set_http_status_code({"message":"user deleted successfully !!!"},200)
        else: return jsonify({"message":"something went wrong !!!"},400)

class Users(Resource):
    def get(self):
        users=db.users.find({})
        temp=[]
        for i,user in enumerate(users):
            temp.append(user)
            temp[i]['_id']=str(temp[i]['_id'])
        return set_http_status_code(temp,200)
    
    def post(self):
        data=json.loads(request.data)
        if len(data)==3 and 'name' in data and 'email' in data and 'password' in data and data['name'] and data['email'] and data['password']: # we can able to reduce this line and output will be same if we use marshmallow
            name=data['name']
            email=data['email']
            password=generate_password_hash(data['password'])
            check=db.users.find_one({"email":email})
            if check is None:
                id=db.users.insert_one({"name":name,"email":email,"password":password})
                return set_http_status_code({"message":"user added successfully."},200)
            else: return set_http_status_code({"message":"user already exist !!!"},400)
        return set_http_status_code({"message":"please enter a valid data !!!"},403)

def set_http_status_code(data,code):
    resp=jsonify(data)
    resp.status_code=code
    return resp

api.add_resource(User,'/<id>')
api.add_resource(Users,'')