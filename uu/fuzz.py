#!/usr/bin/env python3

import afl
import os
import sys
import tempfile
import uu


def fuzz(workfile_in, workfile_out):
    with open(sys.argv[1], "rb") as fp:
        data_orig = fp.read()
    out_decode = workfile_in
    out_encode = workfile_out
    try:
        uu.decode(sys.argv[1], out_decode, mode=0o600, quiet=True)
    except uu.Error:
        pass
    uu.encode(sys.argv[1], out_encode)
    uu.decode(out_encode, out_decode, mode=0o600)
    with open(out_decode, "rb") as fp:
        data_encdec = fp.read()
    assert data_orig == data_encdec


workfile_in = tempfile.NamedTemporaryFile(dir="/dev/shm", delete=False).name
workfile_out = tempfile.NamedTemporaryFile(dir="/dev/shm", delete=False).name

try:
    while afl.loop():
        fuzz(workfile_in, workfile_out)
finally:
    try:
        os.unlink(workfile_in)
    except:
        pass
    try:
        os.unlink(workfile_out)
    except:
        pass
