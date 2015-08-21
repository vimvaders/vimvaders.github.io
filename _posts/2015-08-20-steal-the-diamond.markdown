---
layout: post
title:  "Hackcon 2015: Steal the Diamond"
categories: hackcon2015
tags: crypto
date: 2015-08-20 14:00:00
---

> Category: *crypto* - Points: *25*

The description is provided in the following file:

    D4RKBLU3 is a novice cracker and is starting to learn the basics of Cryptography.
    He comes across this encryption system which uses the following python function to encrypt data:

{% highlight python %}
def enc(message, key):
    message = message.decode('hex')
    key = key.decode('hex')
    return (''.join(chr(ord(k)^ord(c)) for c,k in zip(message,itertools.cycle(key)))).encode('hex')
{% endhighlight %}

    D4RKBLU3 used this function to encode the message "omg thisisfoobar" with two keys.

    He tried devising a complex system which he claims cannot be broken.
    He just provided us with the following flowchart and the final result after using 2 layer encryption.

                  a
                 / \
          key1  /   \  key2
               /     \
              b       c
               \     /
          key2  \   /  key1
                 \ /
                  d


        a = "omg thisisfoobar"
        d = "0b59154b16041c400e1c121f180c0416"

    He used the above mentioned system in such a way that enc(b,c) gave out his password. Are you smart enough to find his password?

When we analyze the `enc` function, we discover that it just repeats the key to make it as long as the message and then xor the two.

From the image we can easily derive the definitions:

$$ a = b \oplus key1 = c \oplus key2 $$

$$ d = b \oplus key2 = c \oplus key1 $$

and also:

$$ b = a \oplus key1 = d \oplus key2 $$

$$ c = a \oplus key2 = d \oplus key1 $$

We need to get $$ b \oplus c $$. Remembering that $$ x \oplus x = 0 $$, we can do:

$$ b \oplus c = ( a \oplus key1 ) \oplus ( d \oplus key1 ) = $$

$$ = a \oplus d \oplus ( key1 \oplus key1 ) = a \oplus d $$

This means that we can just compute $$ a \oplus d $$ to get $$ b \oplus c $$ (the flag):

{% highlight python %}
import itertools

def enc(message, key):
    ...

a = "omg thisisfoobar"
d = "0b59154b16041c400e1c121f180c0416"

# we need to encode *a* since it is then decoded by the function *enc*
print enc(a.encode('hex'), d)
{% endhighlight %}

This gives the following hex string:

    6434726b626c7533676f7470776e6564

which decodes to:

    d4rkblu3gotpwned

<script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"> </script>

