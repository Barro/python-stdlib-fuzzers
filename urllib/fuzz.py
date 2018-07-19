#!/usr/bin/env python3

import afl
import os
import sys
import urllib.parse
import urllib.robotparser


def fuzz():
    with open(sys.argv[1], "rb") as fp:
        data = fp.read(8192)
    data_str = data.decode("utf-8", errors="surrogateescape")

    urllib.parse.unquote_to_bytes(data)
    quoted = urllib.parse.quote_from_bytes(data)
    unquoted = urllib.parse.unquote_to_bytes(quoted)
    assert data == unquoted

    urllib.parse.unquote(data_str)
    urllib.parse.unquote_plus(data_str)

    quoted_str = urllib.parse.quote(
        data_str, errors="surrogateescape")
    unquoted_str = urllib.parse.unquote(
        quoted_str, errors="surrogateescape")
    assert data_str == unquoted_str
    quoted_plus_str = urllib.parse.quote_plus(
        data_str, errors="surrogateescape")
    unquoted_plus_str = urllib.parse.unquote_plus(
        quoted_plus_str, errors="surrogateescape")
    assert data_str == unquoted_plus_str

    try:
        parsed = urllib.parse.urlparse(data_str)
    except ValueError:
        parsed = None
    if parsed:
        urllib.parse.urlunparse(parsed)

    try:
        split = urllib.parse.urlsplit(data_str)
    except ValueError:
        split = None
    if split:
        urllib.parse.urlunsplit(split)

    try:
        urllib.parse.urldefrag(data)
    # TODO documentation is missing here.
    except ValueError:
        pass

    parsed = urllib.parse.parse_qsl(data_str, errors="surrogateescape")
    encoded = urllib.parse.urlencode(parsed, errors="surrogateescape")
    parsed_again = urllib.parse.parse_qsl(encoded, errors="surrogateescape")
    assert parsed == parsed_again, (parsed, parsed_again)
    encoded_again = urllib.parse.urlencode(
        parsed_again, errors="surrogateescape")
    assert encoded == encoded_again, (encoded, encoded_again)


afl.init()
fuzz()
os._exit(0)
