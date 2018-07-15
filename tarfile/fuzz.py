import afl
import sys
import tarfile


def fuzz():
    with open(sys.argv[1], "rb") as fp:
        try:
            with tarfile.open(mode="r:", fileobj=fp) as tp:
                members = tp.getmembers()
                list(tp.getnames())
                for member in members:
                    member.tobuf()
                    tp.extractfile(member)
                    repr(member)
                for name in tp.getnames():
                    pass
                repr(tp)
        except tarfile.TarError:
            pass


while afl.loop():
    fuzz()
