#!/usr/bin/env python3

import afl
import _pydecimal as decimal_py
import _decimal as decimal_c
import math
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()
    try:
        dp = decimal_py.Decimal(data)
        dc = decimal_c.Decimal(data)
    except ValueError:
        return
    except ZeroDivisionError:
        return
    except (decimal_py.InvalidOperation, decimal_c.InvalidOperation):
        return
    assert repr(dp) == repr(dc)
    assert dp.is_canonical() == dc.is_canonical()
    assert dp.is_finite() == dc.is_finite()
    assert dp.is_infinite() == dc.is_infinite()
    assert dp.is_nan() == dc.is_nan()
    assert dp.is_normal() == dc.is_normal()
    assert dp.is_snan() == dc.is_snan()
    assert dp.is_qnan() == dc.is_qnan()
    assert dp.is_signed() == dc.is_signed()
    assert dp.is_subnormal() == dc.is_subnormal()
    assert dp.is_zero() == dc.is_zero()
    try:
        assert repr(dp + dp) == repr(dc + dc)
        assert repr(dp - dp) == repr(dc - dc)
        assert repr(dp * dp) == repr(dc * dc)
        assert repr(dp.adjusted()) == repr(dc.adjusted())
        assert repr(dp.as_tuple()) == repr(dc.as_tuple())
        assert repr(dp.canonical()) == repr(dc.canonical())
        assert repr(dp.compare(dp)) == repr(dc.compare(dc))
        assert repr(dp.conjugate()) == repr(dc.conjugate())
        assert repr(dp.copy_abs()) == repr(dc.copy_abs())
        assert repr(dp.copy_negate()) == repr(dc.copy_negate())
        assert repr(dp.copy_sign(dp)) == repr(dc.copy_sign(dc))
        assert repr(dp.exp()) == repr(dc.exp())
        assert repr(dp.fma(1, 1)) == repr(dc.fma(1, 1))
        assert repr(dp.ln()) == repr(dc.ln())
        assert repr(dp.log10()) == repr(dc.log10())
        assert repr(dp.logb()) == repr(dc.logb())
        assert repr(dp.logical_and(dp)) == repr(dc.logical_and(dc))
        assert repr(dp.logical_invert()) == repr(dc.logical_invert())
        assert repr(dp.logical_or(dp)) == repr(dc.logical_or(dc))
        assert repr(dp.logical_xor(dp)) == repr(dc.logical_xor(dc))
        assert repr(dp.max(dp)) == repr(dc.max(dc))
        assert repr(dp.max_mag(dp)) == repr(dc.max_mag(dc))
        assert repr(dp.min(dp)) == repr(dc.min(dc))
        assert repr(dp.min_mag(dp)) == repr(dc.min_mag(dc))
        assert repr(dp.next_minus()) == repr(dc.next_minus())
        assert repr(dp.next_plus()) == repr(dc.next_plus())
        assert repr(dp.next_toward(dp)) == repr(dc.next_toward(dc))
        assert repr(dp.normalize()) == repr(dc.normalize())
        assert repr(dp.number_class()) == repr(dc.number_class())
        assert repr(dp.quantize(dp)) == repr(dc.quantize(dc))
        assert repr(dp.radix()) == repr(dc.radix())
        assert repr(dp.remainder_near(dp)) == repr(dc.remainder_near(dc))
        assert repr(dp.rotate(dp)) == repr(dc.rotate(dc))
        assert repr(dp.same_quantum(dp)) == repr(dc.same_quantum(dc))
        assert repr(dp.scaleb(dp)) == repr(dc.scaleb(dc))
        assert repr(dp.shift(dp)) == repr(dc.shift(dc))
        assert repr(dp.sqrt()) == repr(dc.sqrt())
        assert repr(dp.to_eng_string()) == repr(dc.to_eng_string())
        assert repr(dp.to_integral()) == repr(dc.to_integral())
        assert repr(dp.to_integral_exact()) == repr(dc.to_integral_exact())
        assert repr(dp.to_integral_value()) == repr(dc.to_integral_value())
        try:
            assert repr(dp.as_integer_ratio()) == repr(dc.as_integer_ratio())
            assert repr(round(dp, 1)) == repr(round(dc, 1))
            assert repr(float(dp)) == repr(float(dc))
            assert repr(int(dp)) == repr(int(dc))
            assert repr(math.floor(dp)) == repr(math.floor(dc))
            assert repr(math.ceil(dp)) == repr(math.ceil(dc))
        except OverflowError:
            pass
        except ValueError:
            pass
    except decimal_py.DecimalException:
        pass


while afl.loop():
    fuzz()
