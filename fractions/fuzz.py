#!/usr/bin/env python3

import afl
import fractions
import math
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()
    try:
        fraction = fractions.Fraction(data)
    except ValueError:
        return
    except ZeroDivisionError:
        return
    fraction + fraction
    fraction - fraction
    fraction * fraction
    if fraction != fractions.Fraction(0):
        fraction / fraction
        fraction // fraction
    math.floor(fraction)
    math.ceil(fraction)
    round(fraction, 1)
    fraction.limit_denominator()


while afl.loop():
    fuzz()
