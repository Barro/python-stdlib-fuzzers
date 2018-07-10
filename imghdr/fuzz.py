import afl
import imghdr
import sys

while afl.loop():
    imghdr.what(sys.argv[1])
