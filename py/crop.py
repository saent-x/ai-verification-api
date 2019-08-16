from cv2 import cv2
import fnmatch
import numpy as np
import base64
from PIL import Image
import base64
import io


def isolateFace(image):
    cropped_image = None

    image_array = np.array(image)
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(
        "/home/kelvin/haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
    )

    # Todo: Clarify if we really need to keep track of the multipe faces??
    print("Found {0} Faces!".format(len(faces)))

    if len(faces) <= 0:
        raise ValueError("Expected to find at least one face!")

    # Todo: Fix this!
    for (x, y, w, h) in faces:
        padding = 0.1
        x_w_new, y_h_new = (x+w+int(w*padding)), (y + h + int(h * padding))
        cv2.rectangle(image_array, (x, y, x+w, y+h), (0, 255, 0), 0)
        cropped_image = image.crop((x, y, x_w_new, y_h_new))

    return cropped_image


def cropFaces(images):
    images.selfie = isolateFace(images["selfie"])
    cropped_ids = []

    for id_image in images["ids"]:
        cropped_ids.append(isolateFace(id_image))

    images["ids"] = cropped_ids
    return images
