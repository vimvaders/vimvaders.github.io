---
layout: post
title:  "Hackcon 2015: Making Love To Bugs"
categories: CATEGORY
tags: pwn
date: 2015-08-20 20:00:00
---

> Category: *pwnage* - Points: *25*
>
> Description: *Get your flag [here]({{ site.url }}/assets/hackcon2015/ilovebugs.pyc).*

The task comes with the file [ilovebugs.pyc]({{ site.url }}/assets/hackcon2015/ilovebugs.pyc) which is a compiled python file. We can decompile it using the [`uncompyle2`](https://pypi.python.org/pypi/uncompyle2) package.

    $ uncompyle2 --py -o . ilovebugs.pyc
    +++ okay decompyling ilovebugs.pyc
    # decompiled 1 files: 1 okay, 0 failed, 0 verify failed

So we can now check the content of [`ilovebugs.py`]({{ site.url }}/assets/hackcon2015/ilovebugs.py):

{% highlight python %}
import sys
users = {'admin': '<REDACTED>'}

def register(username, password):
    if username in users:
        return 'User already exits.'
    users[username] = password
    return 'Registered Successfully.'


def login(username, password):
    if username not in users:
        return 'Wrong pin/password'
    if password != users[username]:
        return 'Wrong pin/password'
    if username == 'admin':
        return 'The FLAG is what you entered in the "Pin" field to get here!'
    return 'You must login as admin to get the flag'


def handle_command(command):
    if command not in ('REG', 'LOGIN'):
        return 'Invalid Command!'
    print 'Username:',
    sys.stdout.flush()
    username = raw_input()
    try:
        print 'Pin ([0-9]+):',
        sys.stdout.flush()
        password = input()
    except:
        return 'Please enter a valid password. Pin can only contain digits.'

    if command == 'REG':
        return register(username, password)
    if command == 'LOGIN':
        return login(username, password)


if __name__ == '__main__':
    print 'Hey welcome to the admin panel'
    print 'Commands: REG, LOGIN'
    try:
        print '>',
        sys.stdout.flush()
        command = raw_input()
        print handle_command(command)
        sys.stdout.flush()
    except:
        pass
{% endhighlight %}

The PIN should be in the form `[0-9]+` and in order to enforce that the `input` function is used. By the way, in python 2.x the `input` function **evaluates** the input. Since the admin password can be retrieved as `users['admin']`, when we pass that exact string as PIN, python evaluates it for us, and stores the correct admin password in the `password` variable, allowing the login.

    $ python ilovebugs.py
    Hey welcome to the admin panel
    Commands: REG, LOGIN
    > LOGIN
    Username: admin
    Pin ([0-9]+): users['admin']
    The FLAG is what you entered in the "Pin" field to get here!

So the flag is `users['admin']`.
