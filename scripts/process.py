import base64
from PIL import Image
import os
import face_recognition
import numpy as np
import io
import sys
import math
import base64
import json
import argparse


def error(message):
    print(json.dumps({'type': "error", 'message': message}))
    sys.exit(-1)


def info(message):
    print(json.dumps({'type': "info", "message": message}))


def result(result):
    print(json.dumps({'type': "result", "result": result}))


def compute_score(images):
    selfie_encoding = face_recognition.face_encodings(images['selfie'])[0]

    if len(selfie_encoding) == 0:
        error("No face detected on selfie image")

    id_encodings = []

    for id_image in images["ids"]:
        id_encoding = face_recognition.face_encodings(id_image)

        if len(id_encoding) == 0:
            error("No face detected in id an ID")

        id_encodings.append(id_encoding[0])

    scores = face_recognition.face_distance(id_encodings, selfie_encoding)
    return np.fromiter(map(lambda score: round((1.0 - score) * 100, 2), scores), dtype=np.float).tolist()


parser = argparse.ArgumentParser()
parser.add_argument("args", type=str, help="JSON arguments")
tmp = parser.parse_args().args

if tmp == None:
    error("No args passed")
    sys.exit(-1)

args = json.loads(tmp)

payload = {"ids": []}
payload['selfie'] = face_recognition.load_image_file(args['selfie'])

for id_image_path in args["ids"]:
    image = face_recognition.load_image_file(id_image_path)
    payload["ids"].append(image)
    
info("Loaded images successfully!")
scores = compute_score(payload)
result(scores)
