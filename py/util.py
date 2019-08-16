import sys
import json

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