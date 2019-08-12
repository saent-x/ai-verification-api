import cv2
import pandas as pd
import fnmatch
import numpy
import PIL
import base64
from PIL import Image
import base64
import io

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
output_column = output_table["Image Data"]

for i in range(len(output_table.index)):
    image_data = output_table["Id"][i]

    # transform the byte array into a buffer and create an image from it 
    image = Image.open(image_buffer)
    image_array = np.array(image)
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=3,
        minSize=(100, 100)
    )

    # Todo: Clarify if we really need to keep track of the multipe faces?? 
    print("Found {0} Faces!".format(len(faces)))

    for (x, y, w, h) in faces:
        padding = 0.1
        xnew, ynew = (x-int(w*padding)), (y-int(h*padding))
        x_w_new, y_h_new = (x+w+int(w*padding)), (y + h + int(h * padding))
        cv2.rectangle(image_array, (x, y, x+w, y+h), (0, 255, 0), 0)
        #cropped_image = image[ynew:y_h_new, xnew:x_w_new]
        
        # crop the image 
        cropped_image = image.crop((x, y, x_w_new, y_h_new))
        cropped_image_buffer = io.BytesIO()
        cropped_image.save(cropped_image_buffer, "jpeg")
        cropped_encoded = base64.b64encode(cropped_image_buffer.getbuffer())

        cropped_selfies.append(bytearray(cropped_encoded))

output_table["Cropped Selfie"] =  cropped_selfies

