#!/usr/bin/env python

with open('data') as f:
    data = f.read()

while True:
    try:
        data = data.decode('base64')
        print data
    except:
        break
