---
layout: post
title:  "Hackcon2015: Watch Me Surf The Internet"
categories: hackcon2015
tags: ctf forensics
date: 2015-08-20 15:00:00
---

> Category: *forensics* - Points: *100*
>
> Description: *Get the flag from the pcap file in the directory.*

We are provided the file [`spying.pcapng.gz`]({{ site.url }}/assets/hackcon2015/spying.pcapng.gz). Let's first check if the extension is correct:

{% highlight bash %}
$ file spying.pcapng.gz
spying.pcapng.gz: gzip compressed data, from Unix
{% endhighlight %}

Ok, it seeems so, we can proceed to extract it:

{% highlight bash %}
$ gzip -dv spying.pcapng.gz
spying.pcapng.gz:	   40.5% -- replaced with spying.pcapng
{% endhighlight %}

The *spying.pcapng* uses the new *pcap* format, and can be analysed with `Wireshark`.
As always we first blindly extract the HTTP files from the pcap.

![http objects extraction from Wireshark]({{ site.url }}/assets/hackcon2015/http-objects.png)

There is only one resource, the page `byld.iiitd.edu.in`. We compared the extracted page with the online one but they resulted to be the same.

Then we started analyzing the other packets. There are a lot of HTTPS connections to google and facebook, so we thought about a crypto challenge.

![https connections]({{ site.url }}/assets/hackcon2015/https.png)

But the organizers gave the hint:

> Try not to get lost in SSL packets. The level doesn't expect you to read SSL packets in anyway.

At last we noted something strange. Multiple packets had some strange slightly-over-10000 source ports. Some of the ports were also duplicated.

![connections to reused ports]({{ site.url }}/assets/hackcon2015/reused-ports.png)

They were all directed to the ip address `192.168.64.22` so we used that as filter and write down the source ports:

    10102  10108  10052  10054  10058  10032  10073  10074  10117  10115  10116  10077  10097  10100  10101  10089  10111  10117  10087  10097  10116  10099  10104  10077  10101  10083  10117  10114  10102  10084  10104  10101  10073  10110  10116  10101  10114  10110  10101  10116

As suspected, they are all slightly over `10000`. If we subtract `10000` from each number we end up with a list of values in ASCII range:

    102  108  52  54  58  32  73  74  117  115  116  77  97  100  101  89  111  117  87  97  116  99  104  77  101  83  117  114  102  84  104  101  73  110  116  101  114  110  101  116

Converting them into ASCII we obtain the flag:

    fl46: IJustMadeYouWatchMeSurfTheInternet

------

We can use `tshark` and `python` to solve this programmatically. First we read the `spying.pcapng` file using `tshark` filtering on the ip destination and extracting the source port:

    tshark -r spying.pcapng -Y 'ip.dst == 192.168.64.22' -T fields -e tcp.srcport

Then we can pipe the result into `python` to do the math and print the string:

    ... | python -c 'import sys; print "".join(chr(int(port) - 10000) for port in sys.stdin.readlines())'

