---
layout: post
title:  "Hackcon 2015: Let's Learn Debugging"
categories: hackcon2015
tags: ctf binary
date: 2015-08-20 12:00:00
---

> Category: *binary* - Points: *75*
>
> Description: *The program apparently once could print more than stories.*

We are provided two files:

- [LetsLearnDebugging]({{ site.url }}/assets/hackcon2015/LetsLearnDebugging)

      $ file LetsLearnDebugging
      LetsLearnDebugging: ELF 64-bit LSB  executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=6fd9298971fef3a0bd87537fe2e2308167f33588, not stripped

- [story.txt]({{ site.url }}/assets/hackcon2015/story.txt)

      $ file story.txt
      story.txt: UTF-8 Unicode text

The file `story.txt` contains an extract of the script of the movie [The Hitchhiker's Guide to the Galaxy](https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy):

> "The Babel fish," said The Hitch Hiker's Guide to the Galaxy quietly, "is small, yellow and leech-like, and probably the oddest
thing in the Universe. It feeds on brainwave energy not from its carrier but from those around it. It absorbs all unconscious
mental frequencies from this brainwave energy to nourish itself with. It then excretes into the mind of its carrier a telepathic
matrix formed by combining the conscious thought frequencies with nerve signals picked up from the speech centres of the brain
which has supplied them. The practical upshot of all this is that if you stick a Babel fish in your ear you can instantly understand
anything said to you in any form of language. The speech patterns you actually hear decode the brainwave matrix which
has been fed into your mind by your Babel fish.
> [...]

Nothing interesting here. And if we run `LetsLearnDebugging` the file `story.txt` is printed in the console. If we remove the `story.txt` file we obtain:

    Could not find file.

And if we change the length of the text:

    Don't you dare change your story.

Analyzing the file with `strings` shows some interesting strings such as:

    seems_interesting
    what_is_this
    what_is_that

and also my personal favorite:

    Oooh good. You should always use strings first. Though I won't say always. But who knows what you'll find in plain text. Try doing something else now.

So we think that the flag is somehow generated from the `story.txt` file. Let's start IDA to understand the code better.

**main**
{% highlight c %}
...
int called = 0;
s = (char *)seems_interesting((__int64)&v13, 102);
if ( ptrace(0, 0LL, 0LL, 0LL, v11) == -1 )
{
  meh();
  puts(s);
}
if ( called != 1 )
  meh();
...
{% endhighlight %}

So it generates the string `s` using `seems_interesting`. This is printed only if `ptrace` returns true (never in this case).

**meh**
{% highlight c %}
...
  while ( 1 )
{
  result = (unsigned int)story_pos;
  if ( story_pos > 9398 )
    break;
  putchar(story[(signed __int64)story_pos++]);
}
called = 1;
...
{% endhighlight %}

This reads the story from the `story.txt` file and outputs it on the console. Since `called` is set to `1` the main function only invokes `meh` once.
Let's analyze a bit deeper to understand what is `s`:

**seems_interesting**
{% highlight c %}
...
v4 = malloc(a2 + 1LL);
for ( i = 0; i < a2; ++i )
  *((_BYTE *)v4 + i) = what_is_this(*(_DWORD *)(4LL * i + a1));
*((_BYTE *)v4 + a2) = 0;
return v4;
...
{% endhighlight %}

This seems to generate a string based on the data produced by `what_is_this`.

**what_is_this**
{% highlight c %}
...
v2 = 0;
for ( i = 0; i < (a1 + 9299) / 107; ++i )
  v2 += printf("%c", (unsigned int)story[(signed __int64)story_pos++]);
return v2;
...
{% endhighlight %}

So, as expected, the `seems_interesting` function is generating a string based on the `story` file.

We can use gdb to force the program to print the string `s`:

    $ gdb -q ./LetsLearnDebugging
    Reading symbols from ./LetsLearnDebugging...(no debugging symbols found)...done.
    (gdb) break ptrace
    Breakpoint 1 at 0x400700
    (gdb) run
    Starting program: LetsLearnDebugging

    "The Babel fish ...

    Breakpoint 1, ptrace (request=PTRACE_TRACEME) at ../sysdeps/unix/sysv/linux/ptrace.c:36
    (gdb) return -1
    Make ptrace return now? (y or n) y
    #0  0x0000000000400cea in main ()
    (gdb) continue
    Continuing.
    “Doesn’t anybody in the whole house know where my coat is? ...

    ###
    Nice! Now that's you've started debugging this. See if there's something blatantly weird.
    ###

    [Inferior 1 (process 26703) exited normally]

Ok, so let's see if there is something else *blatantly weird*. Of all the strange-named functions, one is never invoked: `what_is_that`, so let's call it:

    $ gdb -q ./LetsLearnDebugging
    Reading symbols from ./LetsLearnDebugging...(no debugging symbols found)...done.
    (gdb) break main
    Breakpoint 1 at 0x400c22
    (gdb) run
    Starting program: LetsLearnDebugging

    Breakpoint 1, 0x0000000000400c22 in main ()
    (gdb) call what_is_that()

    "The Babel fish ...

    Good. You're almost there. It's just that I'm feelin.. a bit..

What sorcery is that? The program hanged! Let's analyze the function with IDA:

**what_is_that**
{% highlight c %}
...
v12 = seems_interesting((__int64)&v30, 65);
printf("%s", v12);
sleep(0x186A0u);
...
{% endhighlight %}

Ok, so the program is hanging because there is a pretty long sleep there. Let's skip it.

    $ gdb -q ./LetsLearnDebugging
    Reading symbols from ./LetsLearnDebugging...(no debugging symbols found)...done.
    (gdb) break main
    Breakpoint 1 at 0x400c22
    (gdb) run
    Starting program: LetsLearnDebugging

    Breakpoint 1, 0x0000000000400c22 in main ()
    (gdb) break sleep
    Breakpoint 2 at 0x7ffff7ad5d00: file ../sysdeps/unix/sysv/linux/sleep.c, line 42.
    (gdb) call what_is_that()

    "The Babel fish ...

    Good. You're almost there. It's just that I'm feelin.. a bit..

    Breakpoint 2, __sleep (seconds=100000) at ../sysdeps/unix/sysv/linux/sleep.c:42
    (gdb) return
    Make __sleep return now? (y or n) y
    #0  0x0000000000400a35 in what_is_that ()
    (gdb) continue
    Continuing.
    wherever I went. He said it did him ...

    Awesome! Hope you had fun! Here you go: {d3adc0deiS@PaiN}
    [Inferior 1 (process 26738) exited normally]

We finally got our flag: `{d3adc0deiS@PaiN}`

