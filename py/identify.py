import io
from PIL import Image
import argparse
import json

def identify():
    args = json.loads(input())
    prefix, storage_type, credentials = None, None, None

    if "prefix" in args == False:
        raise ValueError("prefix is required")
    prefix = args["prefix"]

    if "storageType" in args == False:
        raise ValueError("storageType is required")
    storage_type = args["storageType"]

    print("prefix: {}".format(prefix))
    print("storageType: {}".format(storage_type))

identify()