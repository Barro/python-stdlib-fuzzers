#!/usr/bin/env python3

import afl
import netrc
import os
import sys

while afl.loop():
    os.chmod(sys.argv[1], 0o600)
    try:
        nrc = netrc.netrc(sys.argv[1])
    except netrc.NetrcParseError:
        continue
    for host in nrc.hosts:
        nrc.authenticators(host)
