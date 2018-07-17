#!/usr/bin/env python3

import afl
import shlex
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()

    try:
        shlex.split(data)
    # TODO ValueError is not documented.
    except ValueError:
        pass
    data_list = shlex.split(shlex.quote(data))
    assert len(data_list) == 1
    assert data == data_list[0]
    lex = shlex.shlex(infile=sys.argv[1], posix=False)
    while lex.get_token():
        pass
    lex = shlex.shlex(infile=sys.argv[1], posix=True)
    while lex.get_token():
        pass


while afl.loop():
    fuzz()
