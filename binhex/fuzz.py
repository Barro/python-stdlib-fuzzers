#!/usr/bin/env python3

import afl
import binhex
import io
import os
import sys
import tempfile


class CloseIgnoringBytesIO(io.BytesIO):
    def close(self):
        pass


def fuzz(workfile_in, workfile_out):
    # Only copy the first 8 kilobytes to limit the corpus file sizes:
    with open(sys.argv[1], "rb") as ifp, open(workfile_in, "wb") as ofp:
        ofp.write(ifp.read(8 * 1024))

    try:
        binhex.hexbin(workfile_in, "/dev/null")
    except binhex.Error:
        pass

    with open(workfile_in, "rb") as fp:
        data = fp.read()
    out_hex = CloseIgnoringBytesIO()
    binhex.binhex(workfile_in, out_hex)
    infile = io.BytesIO(out_hex.getvalue())
    binhex.hexbin(infile, workfile_out)
    with open(workfile_out, "rb") as fp:
        data_new = fp.read()
    assert data == data_new


# binhex module actually cares about the file name length, so too long
# files are problematic. Use shorter temporary file names instead.
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
