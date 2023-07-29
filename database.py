from app import app
from pymongo import MongoClient


app.config['MONGO_URI']='mongodb://localhost:27017/'
mongo=MongoClient(app.config['MONGO_URI'])
db=mongo.corider # here corider is my database name 