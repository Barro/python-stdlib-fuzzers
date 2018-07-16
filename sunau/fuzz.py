#!/usr/bin/env python3

import afl
import os
import sunau
import sys

# TODO looks like there is a global state within this module as
# afl.loop() is not stable.
afl.init()
try:
    with sunau.open(sys.argv[1]) as fd:
        fd.getnchannels()
        fd.getsampwidth()
        fd.getframerate()
        nframes = fd.getnframes()
        fd.getcomptype()
        fd.getcompname()
        fd.getparams()
        for frame in range(nframes):
            fd.readframes(1)
        fd.tell()
        fd.setpos(0)
        fd.rewind()
except EOFError:
    pass
except sunau.Error:
    pass

os._exit(0)
