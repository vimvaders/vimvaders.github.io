---
layout: post
title:  "Hackcon 2015: Ninja Turtles"
categories: hackcon2015
tags: misc
---

> Category: *Misc* - Points: *25*
>
> Description: *Ninja Turtles*

We are provided the file [ninjaturtles.txt]({{ site.url }}/assets/hackcon2015/ninjaturtles.txt) which contains four kinds of commands with some value:

    Turn left by 90 degrees
    Turn right by 90 degrees
    Go forward 1 spaces
    Go back 200 spaces

These commands are grouped in five blocks separated by empty lines. The last line is:

    Can you digest the message?

The name of the challenge and the kind of commands made us think about the python [`turtle`](https://docs.python.org/2/library/turtle.html) library:

> Turtle graphics is a popular way for introducing programming to kids. It was part of the original Logo programming language developed by Wally Feurzig and Seymour Papert in 1966.
>
> Imagine a robotic turtle starting at (0, 0) in the x-y plane. After an import turtle, give it the command turtle.forward(15), and it moves (on-screen!) 15 pixels in the direction it is facing, drawing a line as it moves. Give it the command turtle.right(25), and it rotates in-place 25 degrees clockwise.
>
> By combining together these and similar commands, intricate shapes and pictures can easily be drawn.

The idea is to interpret the lines into turtle commands in order to draw the shapes. The blocks represents different shapes, so at the end of each block we will make our script pause so that the shape can be identified. We wrote a python utility to interpret the commands:

[**ninjaturtles.py**]({{ site.url }}/assets/hackcon2015/ninjaturtles.py)

{% highlight python %}
import turtle
import time
import re

parse = re.compile(r'([\w ]+) (\d+)')
turtle.mode('logo')

actions = {
    'Turn left by': turtle.left,
    'Turn right by': turtle.right,
    'Go forward': turtle.forward,
    'Go back': turtle.backward
}

with open('ninjaturtles.txt') as data:
    for command in data:
        try:
            action, unit = parse.match(command).groups()
            actions[action](float(unit))
        except:
            # new letter or comment
            time.sleep(5)
            turtle.reset()
{% endhighlight %}

The resulting shapes compose the word `SLASH`:

<img src="{{ site.url }}/assets/hackcon2015/ninja1.png" alt="ninja-1" style="width: 80px;"/> | <img src="{{ site.url }}/assets/hackcon2015/ninja2.png" alt="ninja-2" style="width: 80px;"/> | <img src="{{ site.url }}/assets/hackcon2015/ninja3.png" alt="ninja-3" style="width: 80px;"/> | <img src="{{ site.url }}/assets/hackcon2015/ninja4.png" alt="ninja-4" style="width: 80px;"/> | <img src="{{ site.url }}/assets/hackcon2015/ninja5.png" alt="ninja-5" style="width: 80px;"/>

The final line of the challenge reads `Can you digest the message?` so the flag is obtained by applying the [*MD5 message-digest*](https://en.wikipedia.org/wiki/MD5) algorithm on `SLASH`, resulting in:

    646da671ca01bb5d84dbb5fb2238dc8e

