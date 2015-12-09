---
layout: post
title:  "Seccon 2015: Last Challenge"
categories: seccon2015
tags: ctf misc
date: 2015-12-09 20:00:00
---

> Category: *Misc* - Points: *50*
>
> Description:<br />
> ex1<br />
> Cipher:PXFR}QIVTMSZCNDKUWAGJB{LHYEO<br />
> Plain: ABCDEFGHIJKLMNOPQRSTUVWXYZ{}<br />
>
> ex2<br />
> Cipher:EV}ZZD{DWZRA}FFDNFGQO<br />
> Plain: {HELLOWORLDSECCONCTF}<br />
>
> quiz<br />
> Cipher:A}FFDNEA}}HDJN}LGH}PWO<br />
> Plain: ??????????????????????<br />

The last challenge in Seccon 2015 was exactly the same as the [first one]({{ site.url }}/seccon2015/2015/12/09/start.html). It is still a [*substitution cipher*](https://en.wikipedia.org/wiki/Substitution_cipher) and we have to decode the last message. The substitution pattern is different from the other challenge but we can use the same approach.

We wrote the following python [script]({{ site.url }}/assets/seccon2015/last.py), using [`maketrans`](https://docs.python.org/2/library/string.html#string.maketrans) and [`translate`](https://docs.python.org/2/library/string.html#string.translate).

{% highlight python %}
#!/usr/bin/env python

from string import translate, maketrans

table = maketrans('PXFR}QIVTMSZCNDKUWAGJB{LHYEO', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}')
cipher = 'A}FFDNEA}}HDJN}LGH}PWO'
print translate(cipher, table)
{% endhighlight %}

We then execute the script:

    $ ./last.py
    SECCON{SEEYOUNEXTYEAR}

So the flag is: `SECCON{SEEYOUNEXTYEAR}`

![xkcd](http://imgs.xkcd.com/comics/security.png)
