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
        

        return "Embeddings created for this user"


class CompareFaceEmbeddings(Resource):
    def post(self):
        """ 
        Compare Face embeddings
        ---
        swagger_from_file: static/swagger/face/compare.yml
        """
        try:
            file = request.files['file']
            distance_threshold = request.form.get("threshold")
            if distance_threshold in ["", None]:
                distance_threshold = 0.4
            else:
                distance_threshold = float(distance_threshold)

            file.save(file.filename)

            ebmeddings = create_embeddings(file.filename)
            
            os.remove(file.filename)
            user = "No user found"
            for user_data in users.find():
                distance = compare_embeddings(user_data['embeddings'], ebmeddings)

                if distance < distance_threshold:
                    user = user_data['name']    
                    break    
            return user
        except Exception as ex:
            return str(ex)