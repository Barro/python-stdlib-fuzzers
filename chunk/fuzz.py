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
            cd.read()
            cd.skip()
            cd.read()
            cd.close()
        except EOFError:
            pass
        except MemoryError:
            pass
