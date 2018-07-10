import afl
import sndhdr
import sys

while afl.loop():
    sndhdr.what(sys.argv[1])
    sndhdr.whathdr(sys.argv[1])
