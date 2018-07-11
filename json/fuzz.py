import afl
import json
import json.decoder
import sys

# Enforce Python implementation of the scanstring function:
json.decoder.scanstring = json.decoder.py_scanstring

while afl.loop():
    try:
        data = json.load(open(sys.argv[1], errors="surrogateescape"))
    except RecursionError:
        continue
    except json.decoder.JSONDecodeError:
        continue
    json.dumps(data)
