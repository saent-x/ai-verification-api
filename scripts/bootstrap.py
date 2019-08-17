import argparse
import json
import sys
from azure_hook import fetchImages as fetchAzureImages
from crop import cropFaces
from compute_score import compute_score
import util

def runIdentification(images):
    util.info("Running identification...")
    croppedImages = cropFaces(images)
    score = compute_score(croppedImages)
    util.result(score)

def runVerification(images):
    pass

parser = argparse.ArgumentParser()
parser.add_argument("args", type=str, help="JSON arguments")
tmp = parser.parse_args().args

if tmp == None:
    print("Error!")
    sys.exit(-1)
    
args = json.loads(tmp)

print("prefix: {}".format(args["prefix"]))
print("storage: {}".format(args["storage"]))
print("mode: {}".format(args["mode"]))

if args["storage"] == "azure" and "connectionString" not in args:
    print("Error: You need to specify the conn string")
    sys.exit(-1)
else:
    print("azure connection string: {}".format(args["connectionString"]))

images = fetchAzureImages(args["prefix"], args["connectionString"], args["container"])

if args["mode"] == "identification":
    runIdentification(images)

