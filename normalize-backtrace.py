#!/usr/bin/env python3

import os.path
import sys

lines = sys.stdin.read().splitlines()

if not lines:
    sys.exit(0)

print(lines[0])
next_to_backtrace_line = None

for line in lines[1:]:
    if not line.startswith('  '):
        next_to_backtrace_line = line
        break
    if not line.startswith('  File "'):
        print(line)
        continue
    parts = line.split('"')
    filename = '"'.join(parts[1:-1])
    basename = os.path.basename(filename)
    parts[1:-1] = [basename]
    print('"'.join(parts))

if next_to_backtrace_line:
    if ":" in next_to_backtrace_line:
        exception_type, _ = next_to_backtrace_line.split(":", 1)
        print(exception_type)
    else:
        print(next_to_backtrace_line)
