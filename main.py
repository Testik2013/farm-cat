from settings import *
from game.cat import Cat
from game.world import *
from game.inventory import Inventory
from game.effects import Effects
from game.menu import Menu

STATE = "menu"
menu = Menu([
    ("continue", "Продовжити"),
    ("new",      "Нова гра"),
    ("settings", "Налаштування"),
    ("quit",     "Вийти"),
])
# ╭────────────────────────     Ігрові обʼєкти    ─────────────────────────────╮
# ╰────────────────────────────────────────────────────────────────────────────╯
player = Cat(1, 1)
GROUND_MAP = [
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111222222221111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
    "1111111111111111111111111",
]
OBJECT_MAP = [
    "...........h..............",
    "..........hhh.............",
    "...........h..............",
    "..........................",
    "........h................h",
    "..........................",
    ".....h....................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
    "..........................",
]
world = TileWorld(GROUND_MAP, OBJECT_MAP, show_grid=False)
inventory = Inventory([
    {"code": "h", "name": "Hut",  "count": 80},
    {"code": "t", "name": "Tree", "count": 10},
    {"code": "r", "name": "Rock", "count": 10},
    {"code": "w", "name": "Water","count": 15},
])
effects = Effects()
# ╭────────────────────────      Ігровий цикл     ─────────────────────────────╮
# ╰────────────────────────────────────────────────────────────────────────────╯

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            inventory.select_by_key(e.key)
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            gx, gy = e.pos[0] // BLOCK_SIZE, e.pos[1] // BLOCK_SIZE
            it = inventory.get_selected()
            if it and world.in_bounds(gx, gy) and world.get_obj(gx, gy) == world.EMPTY:
                world.set_obj(gx, gy, it["code"])
                inventory.consume_selected(1)

            # ПКМ: прибрати об'єкт
        if e.type == MOUSEBUTTONDOWN and e.button == 3:
            gx, gy = e.pos[0] // BLOCK_SIZE, e.pos[1] // BLOCK_SIZE
            if world.in_bounds(gx, gy) and world.get_obj(gx, gy) != world.EMPTY:
                world.clear_obj(gx, gy)
        if STATE == "menu":
            choice = menu.handle_event(e)
            if choice == "quit":
                quit()
            elif choice in ("continue", "new"):
                STATE = "game"

    if STATE == "menu":
        menu.draw(window)
    else:
        # ГРА =====
        dt = clock.tick(60) / 1000.0
        # ------- ЗАДНІЙ ФОН
        # Рендер світу
        if hasattr(world, "draw_under"):
            world.draw_under(window)
        else:
            world.draw(window)

        effects.update(dt)
        effects.draw_under(window)
        # Рух гравця з урахуванням блокерів 2-го шару
        keys = key.get_pressed()
        if hasattr(player, "update") and player.update.__code__.co_argcount >= 3:
            player.update(keys, world, effects)
        else:
            player.update(keys)
        player.reset()
        effects.draw_over(window)
        if hasattr(world, "draw_over"):
            world.draw_over(window)

        # Інвентар поверх усього
        # Передай спрайти другого шару, якщо є: WORLD_OBJECT_SPRITES
        O = globals().get("WORLD_OBJECT_SPRITES", {})
        inventory.draw(window, object_sprites=O)

    display.update()
    clock.tick(60)