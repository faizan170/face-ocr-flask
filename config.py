from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import os
import pymongo

# establish a connection to the MongoDB server
client = pymongo.MongoClient(os.getenv("MONGO_CREDENTIALS", "mongodb://localhost:27017"))

# create a new database
db = client["testdb"]

app = Flask(__name__)
cors = CORS(app)
api = Api(app)