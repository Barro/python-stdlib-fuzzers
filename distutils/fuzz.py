#!/usr/bin/env python3

import afl
import distutils.version
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()

    loose = distutils.version.LooseVersion(data)
    loose == loose
    loose < loose
    repr(loose)
    try:
        strict = distutils.version.StrictVersion(data)
        strict == strict
        strict < strict
    except ValueError:
        strict = None
    repr(strict)


while afl.loop():
    fuzz()
