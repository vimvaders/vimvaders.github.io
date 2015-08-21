---
layout: post
title:  "Hackcon 2015: Frag Grenade"
categories: hackcon2015
tags: misc
---

> Category: *misc* - Points: *50*
>
> Description: *flag is [here]({{ site.url }}/assets/hackcon2015/fragG.zip)*

We are given the [`fragG.zip`]({{ site.url }}/assets/hackcon2015/fragG.zip) and when we extract it we obtain 715 `.shredC` files:

    00M73.shredC 0564G.shredC 08GIC.shredC 0B2GJ.shredC 0E2HD.shredC 0FRDU.shredC 0K842.shredC 0LYRZ.shredC 0S1NG.shredC 0TAKA.shredC 0VQEL.shredC 0XHQ0.shredC 0ZR0M.shredC
01IXJ.shredC 05GXI.shredC 08UKO.shredC 0D70A.shredC 0EQD2.shredC 0H7RW.shredC 0L1FB.shredC 0NUX7.shredC 0T16C.shredC 0V4S9.shredC 0WAAG.shredC 0ZGVW.shredC ...

Let's sample the contents of the first files to have an idea:

**00M73.shredC**
{% highlight c %}
void useless() {

//file12
{% endhighlight %}

**0564G.shredC**
{% highlight c %}
}void useless() {

//file355
{% endhighlight %}

**08GIC.shredC**
{% highlight c %}
    printf("Hahahaha Got you!!!\n");

//file142
{% endhighlight %}

This seems to be a C program divided in multiple fragments. The filename order does not seem to reflect the original order in the C source file (which we can suppose is expressed by the last line in each file having format `lineXXX`). We wrote a [this python script]({{ site.url }}/assets/hackcon2015/solve-frag.py) in order to reassemble the file:

{% highlight python %}
from glob import glob
import re

# regular expression to extract the file number from fileXXX
getnum = re.compile(r'//\s*file\s*(\d+)')

def getdata(filename):
    """read the filename and return the file number and its content"""
    with open(filename) as f:
        data = f.read()
        return (int(getnum.search(data).group(1)), data)

# read all the data from the *.shredC files and sort them based on file number
fragments = [getdata(filename) for filename in glob('*.shredC')]
fragments.sort()

# write in the file output.c the concatenation of the fragments
with open('output.c', 'w') as out:
    for chunk_id, chunk_text in fragments:
        out.write(chunk_text + '\n')
        print chunk_id
{% endhighlight %}

We can now inspect the resulting file, which contains a lot of the following blocks:

{% highlight c %}
//file1
void useless() {

//file2
	printf("Hahahaha Got you!!!\n");

//file3
}
{% endhighlight %}

The `main` function instead is:

{% highlight c %}
int main() {
	printf("M");
	printf("Y");
	printf(" ");
	printf("P");
	printf("A");
	printf("S");
	printf("S");
	printf("W");
	printf("O");
	printf("R");
	printf("D");
	printf(" ");
	printf("I");
	printf("S");
	printf(":");
	printf(" ");
	printf("%c",getme1());
	printf("%c",getme2());
	printf("%c",getme3());
	printf("%c",getme4());
	printf("%c",getme5());
	printf("%c",getme6());
	printf("%c",getme7());
	printf("%c",getme8());
	printf("%c",getme9());
	printf("%c",getme10());
	printf("%c",getme11());
	printf("%c",getme12());
	printf("\n");
	printf("Now SHA-256 it and submit");
}
{% endhighlight %}

The `getX()` functions return a single character:

{% highlight c %}
char getme10() {
	return 'a';
}
{% endhighlight %}

By the way if we compile and execute the resulting code we get the following output:

    $ gcc output.c -o output
    $ ./output
    MY PASSWORD IS: Iheartpwnage
    Now SHA-256 it and submit

So we just have to SHA256(Iheartpwnage) to obtain the flag:

    330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

