import sys
import json
import numpy

def info(message):
    payload = {"type": "info", "message": message}
    print(json.dumps(payload))

def error(message):
    payload = {"type": "error", "message": message}
    print(json.dumps(payload))
    sys.exit(-1)

def result(result):
    payload = {"type": "result", "result": result}
    print(json.dumps(payload))
    sys.exit(0)

def numpy_to_cv(pil_image):
    pil_image = pil_image.convert('RGB') 
    open_cv_image = numpy.array(pil_image) 
    # Convert RGB to BGR 
    return open_cv_image[:, :, ::-1].copy() 