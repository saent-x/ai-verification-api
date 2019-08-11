import face_recognition
import numpy as np
import fnmatch
import io
import os
from scipy import ndimage
from PIL import Image
import base64

os.path.join()
def create_mock_input():
    dummy_data = [
        r"123456_id.jpg",
        r"123456_selfie.jpg"
    ]

    dummy_data_2 = [
        b"123456",
        b"123456"
    ]

    return pd.DataFrame({"Images": pd.Series(dummy_data), "Image Data": pd.Series(dummy_data_2)})

input_table = create_mock_input()

output_table = input_table.copy()

scores = []

for i in range(len(output_table.index)):    
	# Obtain the face encodings for the cropped id image
    c_image_data = output_table['Cropped Id'][i]
    # Transform the byte array into a buffer and create an image from it 
    c_image_buffer = io.BytesIO(base64.decodebytes(c_image_data))
    c_image = np.array(Image.open(c_image_buffer))
    c_face_enc = face_recognition.face_encodings(c_image)[0]

    # Obtain the face encodings for the selfie image
    s_image_data = output_table['Selfie'][i]
    # Transform the byte array into a buffer and create an image from it 
    s_image_buffer = io.BytesIO(base64.decodebytes(s_image_data))
    s_image = np.array(Image.open(s_image_buffer))
    s_face_enc = face_recognition.face_encodings(s_image)[0]
    
	# Compares how close the selfie is to the id card image
    score = face_recognition.face_distance([c_face_enc],s_face_enc)[0]
    scores.append(score)

output_table["Score"] = scores

print(scores)