#Embedded file name: hide.py
import os
import random
MESSAGE = os.environ.get('MESSAGE')
x = 18446744073709551616L
r = 29
y = [ not bool(x * r) for x in range(2) ]
algorithm = ['bz2',
 'base64',
 'uu',
 'quopri',
 'zlib'][int(y[0])]
final_strength = random.randint(1, x)

def _encode(message, rounds, strength, encoding):
    for _ in xrange(strength):
        for _ in xrange(rounds):
            message = message.encode(encoding)

    return message


encoded = _encode(MESSAGE, r, final_strength, algorithm)
print encoded
