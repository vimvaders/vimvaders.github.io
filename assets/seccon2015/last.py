#!/usr/bin/env python

from string import translate, maketrans

table = maketrans('PXFR}QIVTMSZCNDKUWAGJB{LHYEO', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}')
cipher = 'A}FFDNEA}}HDJN}LGH}PWO'
print translate(cipher, table)
