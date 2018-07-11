import afl
import configparser
import sys


def fuzz():
    data = open(sys.argv[1], errors="surrogateescape").read()
    parser_basic = configparser.ConfigParser(
        interpolation=configparser.BasicInterpolation())
    try:
        parser_basic.read_string(data)
        for name, proxy in parser_basic.items():
            for option, value in parser_basic.items(name):
                pass
    except configparser.Error:
        pass

    parser_extended = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    try:
        parser_extended.read_string(data)
        for name, proxy in parser_extended.items():
            for option, value in parser_extended.items(name):
                pass
    except configparser.Error:
        pass


while afl.loop():
    fuzz()
