import afl
import csv
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        sniff_data = fp.read(1024)
        try:
            csv.Sniffer().has_header(sniff_data)
            dialect = csv.Sniffer().sniff(sniff_data)
            fp.seek(0)
            reader = csv.reader(fp, dialect)
            for row in reader:
                pass
        except csv.Error:
            pass


while afl.loop():
    fuzz()
