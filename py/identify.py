import io
from PIL import Image
import argparse
import json

# def identify():
#     image_buffer = io.BytesIO(base64.decodebytes(image_data))
#     image = Image.open(image_buffer)

parser = argparse.ArgumentParser()
parser.add_argument("config")
args = parser.parse_args()

payload = json.loads(args.config)
prefix, storage_type = "", ""

if "prefix" in payload == False:
    raise ValueError("prefix is required")
prefix = payload["prefix"]

if "storageType" in payload == False:
    raise ValueError("storageType is required")

storage_type = payload["storageType"]

print("prefix: {}".format(prefix))
print("storageType: {}".format(storage_type))
