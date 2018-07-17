#!/usr/bin/env python3

import afl
import quopri
import sys

orig_a2b_qp = quopri.a2b_qp
orig_b2a_qp = quopri.b2a_qp


def fuzz():
    with open(sys.argv[1], "rb") as fp:
        data = fp.read()

    data_default = quopri.decodestring(data)
    out_tabs_default = quopri.encodestring(data, True)
    assert data == quopri.decodestring(out_tabs_default)
    out_notabs_default = quopri.encodestring(data, False)
    assert data == quopri.decodestring(out_notabs_default)

    quopri.a2b_qp = None
    quopri.b2a_qp = None

    data_python = quopri.decodestring(data)
    assert data_default == data_python

    out_tabs_python = quopri.encodestring(data, True)
    assert data == quopri.decodestring(out_tabs_python)
    out_notabs_python = quopri.encodestring(data, False)
    assert data == quopri.decodestring(out_notabs_python)
    quopri.a2b_qp = orig_a2b_qp
    quopri.b2a_qp = orig_b2a_qp


while afl.loop():
    fuzz()
