from flask_restful import Resource
from src.OCRUtils import engine
from flask import request
from datetime import datetime
from config import db
import os

ocr_col = db.ocr



class OCRView(Resource):
    def post(self):
        """ 
        Face embeddings
        ---
        swagger_from_file: static/swagger/ocr/check.yml
        """

        file = request.files['file']
        name = request.form.get("name")

        file.save(file.filename)

        ocr = engine()
        ocr(file.filename)
        word = ocr.result

        ocr_col.insert_one({
            'filename' : file.filename,
            'data' : word,
            'created_at' : datetime.now()
        })

        os.remove(file.filename)

        return word
