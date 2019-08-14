import face_recognition
import numpy as np
import fnmatch
import io
import os
from PIL import Image
import base64

def compute_score(images):
    # Obtain the face encodings for the cropped id image
    id_encodings = []
    for image in images.ids:
        id_encodings.append(face_recognition.face_encodings(image)[0])

    # Obtain the face encodings for the selfie image
    selfie_encoding = face_recognition.face_encodings(images.selfie)[0]

    # Compares how close the selfie is to the id card image
    scores = 1 - face_recognition.face_distance(id_encodings, selfie_encoding)[0]
    return scores