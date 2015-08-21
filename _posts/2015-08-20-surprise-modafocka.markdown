---
layout: post
title:  "Hackcon 2015: Surprise, Modafocka"
categories: hackcon2015
tags: misc
---

> Category: *misc* - Points: *75*
>
> Description: *[Surprise Surprise]({{ site.url }}/assets/hackcon2015/surprise_muthafuka.jpg)*

The mission comes with the file [surprise_muthafuka.jpg]({{ site.url }}/assets/hackcon2015/surprise_muthafuka.jpg). The extension indicates that this is an image, but when we open it:

![image open error]({{ site.url }}/assets/hackcon2015/image-open-error.png)

Before trying to recover the image we check which file type it really is:

    $ file surprise_muthafuka.jpg
    surprise_muthafuka.jpg: Zip archive data, at least v2.0 to extract

Ok, it's not a file but a zip. Let's unzip it

    $ unzip surprise_muthafuka.jpg
    Archive:  surprise_muthafuka.jpg
    inflating: password.jpg

There is a `password.jpg` file. The name seems promising, but when we open it:

![password.jpg file]({{ site.url }}/assets/hackcon2015/password.jpg)

However, when we open the `password.jpg` file with an hex viewer, the content is more interesting.

![password.jpg hex]({{ site.url }}/assets/hackcon2015/password-hex.png)

Revealing the text:

    Congrats young padawan! Flag for this level is: 3vilf0rce

