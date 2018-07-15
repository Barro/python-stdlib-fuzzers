#!/usr/bin/env python3

import afl
import _pydecimal as decimal
import math
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()
    try:
        d = decimal.Decimal(data)
    except ValueError:
        return
    except ZeroDivisionError:
        return
    except decimal.InvalidOperation:
        return
    repr(d)
    d.is_canonical()
    d.is_finite()
    d.is_infinite()
    d.is_nan()
    d.is_normal()
    d.is_snan()
    d.is_qnan()
    d.is_signed()
    d.is_subnormal()
    d.is_zero()
    try:
        d + d
        d - d
        d * d
        d.adjusted()
        d.as_tuple()
        d.canonical()
        d.compare(d)
        d.conjugate()
        d.copy_abs()
        d.copy_negate()
        d.copy_sign(d)
        d.exp()
        d.fma(1, 1)
        d.ln()
        d.log10()
        d.logb()
        d.logical_and(d)
        d.logical_invert()
        d.logical_or(d)
        d.logical_xor(d)
        d.max(d)
        d.max_mag(d)
        d.min(d)
        d.min_mag(d)
        d.next_minus()
        d.next_plus()
        d.next_toward(d)
        d.normalize()
        d.number_class()
        d.quantize(d)
        d.radix()
        d.remainder_near(d)
        d.rotate(d)
        d.same_quantum(d)
        d.scaleb(d)
        d.shift(d)
        d.sqrt()
        d.to_eng_string()
        d.to_integral()
        d.to_integral_exact()
        d.to_integral_value()
        try:
            d.as_integer_ratio()
            round(d, 1)
            float(d)
            int(d)
            math.floor(d)
            math.ceil(d)
        except OverflowError:
            pass
        except ValueError:
            pass
    except decimal.DecimalException:
        pass


while afl.loop():
    fuzz()
