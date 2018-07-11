import afl
import sys
import wave

while afl.loop():
    try:
        with wave.open(sys.argv[1]) as fd:
            fd.getnchannels()
            fd.getsampwidth()
            fd.getframerate()
            nframes = fd.getnframes()
            fd.getcomptype()
            fd.getparams()
            if nframes > 0:
                fd.readframes(nframes)
            fd.getmarkers()
            fd.rewind()
            fd.setpos(0)
    except wave.Error:
        pass
    except EOFError:
        pass
