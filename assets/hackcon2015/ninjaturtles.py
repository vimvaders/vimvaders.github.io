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

