import afl
import chunk
import sys

while afl.loop():
    with open(sys.argv[1], "rb") as fd:
        try:
            cd = chunk.Chunk(fd)
            cd.getname()
            cd.getsize()
            cd.tell()
            while cd.read(4096):
                pass
            cd.skip()
            while cd.read(4096):
                pass
            cd.close()
        except EOFError:
            pass
