from deepface import DeepFace
import cv2
import numpy as np
from scipy.spatial.distance import cosine



def create_embeddings(image_path):
    try:
        embedding_objs = DeepFace.represent(image_path)
    except Exception as e:
        print("Image Does not contain a face")
        return False
    embedding = embedding_objs[0]["embedding"]

    return embedding



def compare_embeddings(embedding1, embedding2):

    # Calculate the cosine similarity between the two embeddings
    similarity = cosine(embedding1, embedding2)

    return similarity