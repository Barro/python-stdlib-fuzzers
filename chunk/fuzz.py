#!/usr/bin/env python3

import afl
import chunk
import sys


def fuzz():
    with open(sys.argv[1], "rb") as fd:
        try:
            cd = chunk.Chunk(fd)
            cd.getname()
            cd.getsize()
            cd.tell()
            while cd.read(64):
                pass
            cd.skip()
            while cd.read(64):
                pass
            cd.close()
        except EOFError:
            pass


while afl.loop():
    fuzz()
