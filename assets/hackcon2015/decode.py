def decode(message):
    while True:
        try:
            message = message.decode('base64')
        except:
            return message

with open('message.txt') as m:
    print decode(m.read())

