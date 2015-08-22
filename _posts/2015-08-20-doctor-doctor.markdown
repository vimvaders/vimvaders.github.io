---
layout: post
title:  "Hackcon 2015: Doctor Doctor"
categories: hackcon2015
tags: ctf web
date: 2015-08-20 22:00:00
---

> Category: *web* - Points: *25*
>
> Description: *Flag is [here](http://hackcon.in:8080/level8/)*

When we visit the flag [website](http://hackcon.in:8080/level8/) we are greeted with a login form:

![login form]({{ site.url }}/assets/hackcon2015/level8-login.png)

No hints in the source code and everything we try to insert in the form leads miserably to this page (again without hints in the source code):

![message 'you chose poorly' showed after login attempt]({{ site.url }}/assets/hackcon2015/you-chose-poorly.png)

Before embarking on SQLI, we realized that the data inserted in the form is not even submitted to the action page, so there must be something else. Let's check the cookies:

![the page sets two cookies, MadHatter? and MockTurtle?]({{ site.url }}/assets/hackcon2015/cookies.png)

the page sets two cookies, `MadHatter?` and `MockTurtle?` which are both characters from *Alice in wonderland*. Both the cookies contains the same data:

    7fa3b767c460b54a2be4d49030b349c7

A search on Google [showed](http://md5cracker.org/decrypted-md5-hash/7fa3b767c460b54a2be4d49030b349c7) that the string is just the MD5 of `no`. So for the next hour we tried to replace the value of the cookies with other MD5 hashes for `yes`, `maybe`, `ofcourse`, `yeah` and many other (obviously including insults).

Just before going insane we decided to explore the webservice a bit more. We figured that the content of the [robots.txt](http://hackcon.in:8080/level8/robots.txt) file was:

    User-agent: *
    Disallow: /what_is_this_place

So we checked the page at <http://hackcon.in:8080/level8/what_is_this_place>:

![content of the page what_is_this_place showing four files]({{ site.url }}/assets/hackcon2015/what_is_this_place.png)

All the files contain some non-interesting words. We started looking at the file having the name of the first of our two cookies, `MadHatter`, which contained:

    sternutate

Setting the value of the cookie `MadHatter?` to the MD5 of the word `sternutate` (`27a297c35cf0e6930faec429512e2490`) and attempting to login results in:

![MadHatter login]({{ site.url }}/assets/hackcon2015/madhatter.png)

So we checked the content of `MockTurtle`:

    borborygmi

Restoring the value of the cookie `MadHatter?` to its original value and setting the value of the cookie `MockTurtle?` to the MD5 of the word `borborygmi` (`27a297c35cf0e6930faec429512e2490`) and attempting to login results in:

![MockTurtle login]({{ site.url }}/assets/hackcon2015/mockturtle.png)

So our flag is `0901368cc95e06c6067da0ac24c69de2` (which is actually the MD5 of `jabbajabba`).

