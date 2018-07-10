
import afl
import aifc
import sys

while afl.loop():
    try:
        with aifc.open(sys.argv[1]) as fd:
            fd.getnchannels()
            fd.getsampwidth()
            fd.getframerate()
            nframes = fd.getnframes()
            fd.getcomptype()
            fd.getcompname()
            fd.getparams()
            markers = fd.getmarkers()
            if markers:
                for marker in markers:
                    fd.getmark(marker)
            if nframes > 0:
                fd.readframes(nframes)
            fd.tell()
            fd.rewind()
            fd.setpos(0)
    except EOFError:
        pass
    except aifc.Error:
        pass
