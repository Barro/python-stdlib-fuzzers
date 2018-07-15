#!/usr/bin/env python3

import os.path
import sys

for line in sys.stdin.read().splitlines():
    if not line.startswith('  File "'):
        print(line)
        continue
    parts = line.split('"')
    filename = '"'.join(parts[1:-1])
    basename = os.path.basename(filename)
    parts[1:-1] = [basename]
    print('"'.join(parts))
