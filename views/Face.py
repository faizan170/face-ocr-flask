from flask_restful import Resource
from flask import make_response
from src.FaceUtils import create_embeddings, compare_embeddings
from flask import request
from datetime import datetime
from config import db
import os
users = db.users

user_schema = {
    "firstName": str,
    "lastName": str,
    "email": {
        "type": str,
        "required": True,
        "unique": True,
    },
    "mobileNumber": {
        "type": str,
        "unique": True,
    },
    "mPinCode": str,
    "emiratesId": str,
    "countryName": str,
    "userImage": str,
    "faceId": str,
    "nickName": str,
    "idType": str,
    "faceImage": str,
    "avtarId": int,
    "emoji": str,
    "password": {
        "type": str,
        "required": True,
    },
    "verified": {
        "type": bool,
        "default": False,
    },
    "verifyOtp": str,
    "resetOtp": str,
    "stellar": {
        "publicKey": {
            "type": str,
            "default": None,
        },
        "secretKey": {
            "iv": {
                "type": str,
                "default": None,
            },
            "key": {
                "type": str,
                "default": None,
            },
            "secretKey": {
                "type": str,
                "default": None,
            },
        },
    },
    "face_embedding": list
}


def process_key(keyData):
    if type(keyData) == dict and keyData.get("type") == None:
        final = {}
        for k, v in keyData.items():
            final[k] = process_key(v)
        return final
    elif type(keyData) == dict and keyData.get("type") != None:
        return None
    return None

class FaceEmbeddings(Resource):
    def post(self):
        """ 
        Face embeddings
        ---
        swagger_from_file: static/swagger/face/embeddings.yml
        """
        try:
            file = request.files['file']
            name = request.form.get("name", "")

            # Split name to first and last name
            firstName = name.split(" ")[0]
            lastName = name.replace(f"{name.split(' ')[0]} ", "") if len(name.split(" ")) > 1 else None

            file.save(file.filename)

            # Get embeddings
            try:
                ebmeddings = create_embeddings(file.filename)
            except:
                os.remove(file.filename)
                return make_response("No embeddings found", 400)
            
            os.remove(file.filename)
            if not ebmeddings:
                return make_response("No embeddings found", 400)


            available_data = {
                "firstName" : firstName if len(firstName) > 0 else None,
                "lastName" : lastName,
                'face_embedding' : ebmeddings,
                'created_at' : datetime.now()
            }
            for key, val in user_schema.items():
                if key not in available_data:
                    available_data[key] = process_key(val)

            
            users.insert_one(available_data)
            

            return "Embeddings created for this user"
        except:
            return make_response("Failed to add embeddings", 200)


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
                distance = compare_embeddings(user_data['face_embedding'], ebmeddings)

                if distance < distance_threshold:
                    user = f"{user_data['firstName']} {user_data.get('lastName', '')}".replace("None", "")
                    break    
            return user.strip()
        except Exception as ex:
            return str(ex)