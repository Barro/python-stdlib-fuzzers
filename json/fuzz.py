#!/usr/bin/env python3

import afl
import json
import json.decoder
import sys

orig_scanstring = json.decoder.scanstring

while afl.loop():
    try:
        data_default = json.load(open(sys.argv[1], errors="surrogateescape"))
        # Enforce Python implementation of the scanstring function:
        json.decoder.scanstring = json.decoder.py_scanstring
        data_python = json.load(open(sys.argv[1], errors="surrogateescape"))
        assert data_default == data_python
    except RecursionError:
        continue
    except json.decoder.JSONDecodeError:
        continue
    finally:
        json.decoder.scanstring = orig_scanstring
    json.dumps(data_default)
