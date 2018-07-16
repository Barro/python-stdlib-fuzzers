import afl
import os
import re
import sys


def fuzz():
    with open(sys.argv[1], "rb") as fp_bytes:
        data_bytes = fp_bytes.read()
    with open(sys.argv[1], errors="surrogateescape") as fp_str:
        data_str = fp_str.read()
    try:
        re.compile(data_bytes)
    except re.error:
        pass
    try:
        re.compile(data_str)
    except re.error:
        pass


afl.init()
fuzz()
os._exit(0)
