from config import api
from views.Face import (
 FaceEmbeddings, CompareFaceEmbeddings
)
from views.OCR import (
    OCRView
)

api.add_resource(FaceEmbeddings, "/api/v1/create-embeddings")
api.add_resource(CompareFaceEmbeddings, "/api/v1/compare")


api.add_resource(OCRView, "/api/v1/ocr")