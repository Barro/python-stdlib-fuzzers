#!/usr/bin/env python3

import afl
import base64
import sys


def fuzz(filename):
    with open(filename, "rb") as fp:
        data = fp.read()
    try:
        base64.b64decode(data)
    except base64.binascii.Error:
        pass
    try:
        base64.standard_b64decode(data)
    except base64.binascii.Error:
        pass
    try:
        base64.urlsafe_b64decode(data)
    except base64.binascii.Error:
        pass
    try:
        base64.b32decode(data)
    except base64.binascii.Error:
        pass
    try:
        base64.b16decode(data)
    except base64.binascii.Error:
        pass
    try:
        base64.a85decode(data)
    # TODO undocumented exception.
    except ValueError:
        pass
    try:
        base64.a85decode(data, adobe=True)
    # TODO undocumented exception.
    except ValueError:
        pass
    try:
        base64.b85decode(data)
    # TODO undocumented exception.
    except ValueError:
        pass

    assert data == base64.b64decode(base64.b64encode(data))
    assert data == base64.standard_b64decode(base64.standard_b64encode(data))
    assert data == base64.urlsafe_b64decode(base64.urlsafe_b64encode(data))
    assert data == base64.b32decode(base64.b32encode(data))
    assert data == base64.b16decode(base64.b16encode(data))
    assert data == base64.a85decode(base64.a85encode(data))
    assert data == base64.a85decode(
        base64.a85encode(data, adobe=True), adobe=True)
    assert data == base64.b85decode(base64.b85encode(data))


# Initialize global state:
fuzz("/dev/null")

while afl.loop():
    fuzz(sys.argv[1])
