### Actions ###
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

actions = [UP, DOWN, LEFT, RIGHT]

### Cells ###
EMPTY = 0
START = 1
TRAP = 6
WALL = 7
PLAYER = 8
GOAL = 9

cell_unicode = [u'\u25a1', u'\u0391', 2, 3, 4, 5, u'\u203b', u'\u25a0', u'\u263a', u'\u03a9']

def cell_value_to_unicode(x):
    return cell_unicode[x]
