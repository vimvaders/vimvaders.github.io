---
layout: post
title:  "Hackcon 2015: Pythonista"
categories: hackcon2015
tags: ctf pwn
date: 2015-08-20 21:00:00
author: enrico
---

> Category: *pwn* - Points: *25*
>
> Description: *The program apparently once could print more than stories.*

The task comes with two files:

- [`hide.pyo`]({{ site.url }}/assets/hackcon2015/hide.pyo)
- [`message.txt`]({{ site.url }}/assets/hackcon2015/message.txt)

The file [`message.txt`]({{ site.url }}/assets/hackcon2015/message.txt) seems to contain a *base64* string, but when decoding it, we receive another *base64* string. Let's check the other file to understand what is going on.

The file [`hide.pyo`]({{ site.url }}/assets/hackcon2015/hide.pyo) is a compiled python object file. We can decompile it using the [`uncompyle2`](https://pypi.python.org/pypi/uncompyle2) package.

    $ uncompyle2 --py -o . hide.pyo
    +++ okay decompyling hide.pyo
    # decompiled 1 files: 1 okay, 0 failed, 0 verify failed

So we can now check the content of [`hide.py`]({{ site.url }}/assets/hackcon2015/hide.py):

{% highlight python %}
import os
import random

MESSAGE = os.environ.get('MESSAGE')
x = 18446744073709551616L
r = 29
y = [ not bool(x * r) for x in range(2) ]
algorithm = ['bz2', 'base64', 'uu', 'quopri', 'zlib'][int(y[0])]
final_strength = random.randint(1, x)

def _encode(message, rounds, strength, encoding):
    for _ in xrange(strength):
        for _ in xrange(rounds):
            message = message.encode(encoding)
    return message

encoded = _encode(MESSAGE, r, final_strength, algorithm)
print encoded
{% endhighlight %}

We add some comment in order to understand what is going on:

{% highlight python %}
import os
import random

# get the MESSAGE from the environment variable MESSAGE
MESSAGE = os.environ.get('MESSAGE')
x = 18446744073709551616L
r = 29

y = [ not bool(x * r) for x in range(2) ] # = [1, 0]
algorithm = ['bz2', 'base64', 'uu', 'quopri', 'zlib'][int(y[0])]
# since y[0] = 1, algorithm = 'base64'

# we can not know which random number was chosen here at runtime
final_strength = random.randint(1, x)

# for a number of times rounds*strength,
# replace message with its encoding (nested encoding)
def _encode(message, rounds, strength, encoding):
    for _ in xrange(strength):
        for _ in xrange(rounds):
            message = message.encode(encoding)
    return message

# encode MESSAGE with 29 * final_strength passes of base64
encoded = _encode(MESSAGE, r, final_strength, algorithm)
print encoded
{% endhighlight %}

So we are dealing with multiple passes of base64. The easiest way is to read the file `message.txt` and iterate a base64 decoding, until an exception is raised (meaning that the string is no longer in base64, so it is the original string).

We created [this python script]({{ site.url }}/assets/hackcon2015/decode.py) in order to do that:

{% highlight python %}
def decode(message):
    while True:
        try:
            message = message.decode('base64')
        except:
            return message

with open('message.txt') as m:
    print decode(m.read())
{% endhighlight %}

The result is the following string: [`https://xkcd.com/936/`](https://xkcd.com/936/), which is:

![password strength](http://imgs.xkcd.com/comics/password_strength.png)

So we tried the super-famous `correcthorsebatterystaple` as the flag but it didn't work. The other one was `Tr0ub4dor&3` and it worked, so this is our flag.

