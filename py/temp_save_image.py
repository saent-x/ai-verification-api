import io
import os
import base64
from PIL import Image

SAVE_PATH = r"/h"


def saveImages(prefix, images):
    # Transform the byte array into a buffer and create an image from it
    images.selfie.save(os.path.join(SAVE_PATH, prefix+"_selfie.jpg"))

    count = 0
    for id_image in images.ids:
        id_image.save(os.path.join(
            SAVE_PATH, prefix+"_id{}.jpg".format(count)))
        count = count+1
