#Embedded file name: wtfpython.py
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
