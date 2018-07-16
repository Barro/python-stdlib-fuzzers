#!/usr/bin/env python3

import afl
import email.errors
import mailbox
import sys


def fuzz():
    mail = mailbox.mbox(sys.argv[1])
    for key, value in mail.items():
        try:
            mail.get(key)
        except email.errors.MessageError:
            pass
        try:
            mail.get_message(key)
            mail.get_bytes(key)
            mail.get_string(key)
            mail.get_file(key)
        except KeyError:
            pass
        except email.errors.MessageError:
            pass
    mail.close()


while afl.loop():
    fuzz()
