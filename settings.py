from pygame import *

# ╭───────────────────────────────  Налаштування  ─────────────────────────────╮
# ╰────────────────────────────────────────────────────────────────────────────╯

init()

WIDTH = 1200
HEIGHT = 600
window=display.set_mode((WIDTH,HEIGHT))
clock = time.Clock()


BLOCK_SIZE = 50

# картинки карти
GRASS1 = transform.scale(image.load('assets/images/grasses/Grass.png'), (BLOCK_SIZE, BLOCK_SIZE))
GRASS2 = transform.scale(image.load('assets/images/grasses/Grass2.png'), (BLOCK_SIZE, BLOCK_SIZE))

# картинки об'єктів на карті
HILL = transform.scale(image.load('assets/images/hills/mediumhill.png'), (BLOCK_SIZE, BLOCK_SIZE))
TREE = transform.scale(image.load('assets/images/trees/wedge-tree.png'), (BLOCK_SIZE, BLOCK_SIZE))
ROCK = transform.scale(image.load('assets/images/rocks/smallrock.png'), (BLOCK_SIZE, BLOCK_SIZE))
WATER = transform.scale(image.load('assets/images/justwater/Water.png'), (BLOCK_SIZE, BLOCK_SIZE))

CAT_AFTERWARD = transform.scale(image.load('assets/images/cat/walkcat_afterward.png'), (BLOCK_SIZE, BLOCK_SIZE))
CAT_FORWARD = transform.scale(image.load("assets/images/cat/walkcat_forward.png"), (BLOCK_SIZE, BLOCK_SIZE))
CAT_LEFT = transform.scale(image.load("assets/images/cat/walkcat_left.png"), (BLOCK_SIZE, BLOCK_SIZE))
CAT_RIGHT = transform.scale(image.load("assets/images/cat/walkcat_right.png"), (BLOCK_SIZE, BLOCK_SIZE))
CAT_SPRITES = {
    "down":  CAT_AFTERWARD,
    "up": CAT_FORWARD,
    "right": CAT_RIGHT,
    "left": CAT_LEFT
}