from flask_restful import Resource
from src.OCRUtils import engine
from flask import request
from datetime import datetime, date
from config import db
import os

ocr_col = db.customer

customer_schema = {
    "id": { "type": str },
    "account": { "type": str },
    "memo": { "type": str },
    "muxedAccount": { "type": str },
    #"first_name": { "type": str },
    #"last_name": { "type": str, "required": True },
    "name" : {"type" : str}, # changed from first last name
    "nationality" : {"type" : str},
    "passport_number" : {"type" : str},
    "surname" : {"type" : str},
    "mother_name" : {"type" : str},
    "issuing_authority" : {"type" : str},
    "additional_name": { "type": str },
    "address_country_code": { "type": str },
    "state_or_province": { "type": str },
    "city": { "type": str },
    "postal_code": { "type": str, "required": True },
    "address": { "type": str },
    "mobile_number": { "type": str },
    "email_address": { "type": str },
    "date_of_birth" : {"type" : str}, #"birth_date": { "type": "Date" },
    "place_of_birth" : {"type" : str}, #"birth_place": { "type": str },
    "birth_country_code": { "type": str },
    "bank_account_number": { "type": str },
    "bank_account_type": { "type": str },
    "bank_number": { "type": str },
    "bank_phone_number": { "type": str },
    "bank_branch_number": { "type": str },
    "clabe_number": { "type": str },
    "tax_id": { "type": str },
    "tax_id_name": { "type": str },
    "occupation": { "type": "Number" },
    "employer_name": { "type": str },
    "employer_address": { "type": str },
    "language_code": { "type": str },
    "id_type": { "type": str },
    "id_country_code": { "type": str },
    "date_of_issue" : {"type" : date}, #"id_issue_date": { "type": "Date" },
    "date_of_expiry" : {"type" : date}, #"id_expiration_date": { "type": "Date" },
    "id_number": { "type": str },
    "photo_id_front": { "type": str },
    "photo_id_back": { "type": str },
    "notary_approval_of_photo_id": { "type": "Buffer" },
    "ip_address": { "type": str },
    "photo_proof_residence": { "type": str },
    "sex": { "type": str },
    "proof_of_income": { "type": "Buffer" },
    "proof_of_liveness": { "type": "Buffer" },
    "cbu_number": { "type": str },
    "cbu_alias": { "type": str }
}

class OCRView(Resource):
    def post(self):
        """ 
        Face embeddings
        ---
        swagger_from_file: static/swagger/ocr/check.yml
        """

        file = request.files['file']
        file.save(file.filename)

        ocr = engine()
        ocr(file.filename)
        word = ocr.result

        to_insert = {
            'filename' : file.filename,
            'created_at' : datetime.now()
        }
        to_insert.update(word)
        
        for key, val in customer_schema.items():
            if key not in to_insert:
                to_insert[key] = None



        ocr_col.insert_one(to_insert)

        os.remove(file.filename)

        return word
