import afl
import sys
import zipfile


def fuzz():
    with open(sys.argv[1], "rb") as fp:
        try:
            with zipfile.ZipFile(file=fp, mode="r",) as zp:
                for info in zp.infolist():
                    info.is_dir()
                    repr(info)
                for name in zp.namelist():
                    zp.getinfo(name)
                    zp.read(name)
                    with zp.open(name) as zpp:
                        # Make sure that we do not fail at CRC checks:
                        zpp._expected_crc = None
                        try:
                            zpp.read(4096)
                        # TODO how to determine if the password is needed?
                        except RuntimeError:
                            pass
                        repr(zpp)
                    zp.testzip()
                repr(zp)
        except zipfile.BadZipFile:
            pass
        except zipfile.LargeZipFile:
            pass
        # read() method throws this on unknown compression types:q
        except NotImplementedError:
            pass


while afl.loop():
    fuzz()
