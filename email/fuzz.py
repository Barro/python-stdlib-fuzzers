import afl
import email.parser
import email.policy
import os
import sys


def fuzz(parser):
    with open(sys.argv[1], "rb") as fp:
        message = parser.parse(fp)
    message.as_bytes(policy=email.policy.default)
    message.is_multipart()
    message.get_unixfrom()
    keys = message.keys()
    for key in keys:
        message.get(key)
        message.get_all(key)
    message.values()
    message.get_content_type()
    message.get_content_maintype()
    message.get_content_subtype()
    message.get_default_type()
    message.get_filename()
    message.get_boundary()
    message.get_content_charset()
    message.is_attachment()
    message.get_content_disposition()
    for part in message.walk():
        pass


parser = email.parser.BytesParser(policy=email.policy.default)
parser.parsebytes(b"")
afl.init()
fuzz(parser)
os._exit(0)
