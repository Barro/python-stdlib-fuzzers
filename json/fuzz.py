#!/usr/bin/env python3

import afl
import json
import json.decoder
import sys

orig_make_scanner = json.scanner.make_scanner
orig_scanstring = json.decoder.scanstring
orig_c_make_encoder = json.encoder.c_make_encoder
orig_encode_basestring_ascii = json.encoder.encode_basestring_ascii
orig_encode_basestring = json.encoder.encode_basestring


def fuzz():
    try:
        data_default = json.load(open(sys.argv[1], errors="surrogateescape"))
        # Enforce Python implementation of the scanstring function:
        json.scanner.make_scanner = json.scanner.py_make_scanner
        json.decoder.scanstring = json.decoder.py_scanstring
        data_python = json.load(open(sys.argv[1], errors="surrogateescape"))
    except RecursionError:
        return
    except json.decoder.JSONDecodeError:
        return
    finally:
        json.scanner.make_scanner = orig_make_scanner
        json.decoder.scanstring = orig_scanstring

    try:
        # Make sure that we don't compare different floating point
        # values that are never equal, as float("nan") == float("nan")
        # test results always in false value.
        json.dumps(data_default, allow_nan=False)
    except ValueError:
        return

    assert data_default == data_python
    json.encoder.c_make_encoder = None
    json.encoder.encode_basestring_ascii = json.encoder.py_encode_basestring_ascii
    json.encoder.encode_basestring = json.encoder.py_encode_basestring
    json.dumps(data_default, allow_nan=False)
    json.encoder.c_make_encoder = orig_c_make_encoder
    json.encoder.encode_basestring_ascii = orig_encode_basestring_ascii
    json.encoder.encode_basestring = orig_encode_basestring


while afl.loop():
    fuzz()
