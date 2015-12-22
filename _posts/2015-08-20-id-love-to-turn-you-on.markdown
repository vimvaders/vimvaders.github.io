---
layout: post
title:  "Hackcon 2015: I'd love to turn you on"
categories: hackcon2015
tags: ctf crypto
date: 2015-08-20 13:00:00
author: enrico
---

> Category: *crypto* - Points: *100*
>
> Description: *[Problem Text]({{ site.url }}/assets/hackcon2015/problem.txt)*
>
> Hint1: *The flag is in all uppercase letters without spaces.*

The text of the problem is the following:


    <i>Let's take it from the top</i>

    I-II-III

    <strong>I</strong> read the news today oh boy
    About a lucky man who made the grade
    And though the news was rather sad
    Well I just had to laugh

    <strong>I</strong> saw the photograph.
    He blew his mind out in a car
    He didn't notice that the lights had changed
    A crowd of people stood and stared
    They'd seen his face before
    Nobody was really sure
    If he was from the House of Lords.

    <strong>I</strong> saw a film today oh boy
    <u>The English army had just won the war</u>
    A crowd of people turned away
    But I just had to look
    Having read the book
    I'd love to turn you on, machine


This is just a plain txt, no steganography, no whitespace encoding, nothing. It is just the first part of the lyrics of the song [*A Day In The Life*](https://www.youtube.com/watch?v=P-Q9D4dcYng) by *The Beatles* with some HTML and the trailing `, machine`, not present in the original lyrics.

We actually tried many different things on this text (not even the category of the task was disclosed by the organizers), including different variations on the title of the movie [*How I Won the War*](https://en.wikipedia.org/wiki/How_I_Won_the_War) starring John Lennon and to which the underlined sentence `the English army had just won the war` [refers to](https://en.wikipedia.org/wiki/A_Day_in_the_Life).

Just before the end of the competition the organizers revealed another hint:

> This is a crypto challenge. Only the highlighted parts are important to get to know what you have to do. What you have to do it on, is the name of the song.

At that point, it was clear that the task was related to the [Enigma](https://en.wikipedia.org/wiki/Enigma_machine) machine. In fact, Enigma was *hacked* by [*Alan Turing*](https://en.wikipedia.org/wiki/Alan_Turing), providing a big boost to the English army to win the war.

We found an online Enigma simulator at <http://www.enigmaco.de/enigma/enigma.swf>. The Enigma code has three rotors (named I, II and III as in the problem text), and we set them respectively to `I`, `I` and `I` since those are the three letters in the `&lt;strong&gt;` tags, and the hint said to only consider the highlighted parts of the text. The input to enigma was, as expressed by the hint *What you have to do it on, is the name of the song*, the title of the song, without spaces and uppercase: `ADAYINTHELIFE` producing as output the flag: `XNEIDSWBHACCH`.

![enigma machine]({{ site.url }}/assets/hackcon2015/enigma.png)

