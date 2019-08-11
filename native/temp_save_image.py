import io
import os
import base64
from PIL import Image

output_table = input_table.copy()

SAVE_PATH = r"C:\Users\Mee\Desktop\AI\Identity Verification\Knime Dump"

for i in range(len(output_table.index)):
	# We'll use the has to tag the images when we save them to disk
    hash = output_table["Hash"][i]

    s_image_data = output_table['Selfie'][i]
    # Transform the byte array into a buffer and create an image from it 
    s_image_buffer = io.BytesIO(base64.decodebytes(s_image_data))
    s_image = Image.open(s_image_buffer)
    s_image.save(os.path.join(SAVE_PATH,hash+"_selfie.jpg"))

    i_image_data = output_table['Id'][i]
    # Transform the byte array into a buffer and create an image from it 
    i_image_buffer = io.BytesIO(base64.decodebytes(i_image_data))
    i_image = Image.open(i_image_buffer)
    i_image.save(os.path.join(SAVE_PATH,hash+"_id.jpg"))
    
    c_image_data = output_table['Cropped Id'][i]
    # Transform the byte array into a buffer and create an image from it 
    c_image_buffer = io.BytesIO(base64.decodebytes(c_image_data))
    c_image = Image.open(c_image_buffer)
    c_image.save(os.path.join(SAVE_PATH,hash+"_crop_id.jpg")) 
    