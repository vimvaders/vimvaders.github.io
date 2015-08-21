#!/usr/bin/env python

from glob import glob
import re

# regular expression to extract the file number from fileXXX
getnum = re.compile(r'//\s*file\s*(\d+)')

def getdata(filename):
    """read the filename and return the file number and its content"""
    with open(filename) as f:
        data = f.read()
        return (int(getnum.search(data).group(1)), data)

# read all the data from the *.shredC files and sort them based on file number
frags = [getdata(filename) for filename in glob('fileCompileLevel/*.shredC')]
frags.sort()

# write in the file output.c the concatenation of the fragments
with open('output.c', 'w') as out:
    for chunk_id, chunk_text in frags:
        out.write(chunk_text + '\n')
        print chunk_id

