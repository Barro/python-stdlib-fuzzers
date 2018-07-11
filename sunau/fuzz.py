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
        if nframes > 0:
            fd.readframes(nframes)
        fd.tell()
        fd.setpos(0)
        fd.rewind()
# TODO file.read(nframes * self._framesize) causes large memory
# allocations when nframes is large. This can cause quite possible out
# of memory errors with really small inputs.
except MemoryError:
    pass
except EOFError:
    pass
except sunau.Error:
    pass

os._exit(0)
