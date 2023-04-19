from flask_restful import Resource
from src.FaceUtils import create_embeddings, compare_embeddings
from flask import request
from datetime import datetime
from config import db
import os
users = db.users

class FaceEmbeddings(Resource):
    def post(self):
        """ 
        Face embeddings
        ---
        swagger_from_file: static/swagger/face/embeddings.yml
        """

        file = request.files['file']
        name = request.form.get("name")

        file.save(file.filename)

        ebmeddings = create_embeddings(file.filename)
        
        os.remove(file.filename)

        users.insert_one({
            'name' : name,
            'embeddings' : ebmeddings,
            'created_at' : datetime.now()
        })
        

        print(name, file)


class CompareFaceEmbeddings(Resource):
    def post(self):
        """ 
        Compare Face embeddings
        ---
        swagger_from_file: static/swagger/face/compare.yml
        """

        file = request.files['file']
        distance_threshold = request.form.get("threshold")
        if distance_threshold == "":
            distance_threshold = 0.4
        else:
            distance_threshold = float(distance_threshold)

        file.save(file.filename)

        ebmeddings = create_embeddings(file.filename)
        
        os.remove(file.filename)
        user = "Not Found"
        for user in users.find():
            distance = compare_embeddings(user['embeddings'], ebmeddings)

            if distance < distance_threshold:
                user = user['name']        
        return user