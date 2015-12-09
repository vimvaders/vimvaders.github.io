#!/usr/bin/env python

from string import maketrans, translate

table = maketrans('PXFR}QIVTMSZCNDKUWAGJB{LHYEO', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}')
cipher = 'A}FFDNEVPFSGV}KZPN}GO'
print translate(cipher, table)
