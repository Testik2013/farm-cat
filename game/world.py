# world.py
from settings import *
import pygame as pg

# ---- зіставлення символів ґрунту до зображень, лише якщо є у settings ----
# '1' -> GRASS1, '2' -> GRASS2, '3' -> GRASS3, '4' -> GRASS4
WORLD_GROUND_SPRITES: dict[str, pg.Surface] = {}
for sym, var in (("1", "GRASS1"), ("2", "GRASS2"), ("3", "GRASS3"), ("4", "GRASS4")):
    surf = globals().get(var)
    if surf is not None:
        WORLD_GROUND_SPRITES[sym] = surf  # якщо немає — не додаємо і не малюємо

WORLD_OBJECT_SPRITES: dict[str, pg.Surface] = {}
for sym, var in (("t", "TREE"), ("r", "ROCK"), ("b", "BUSH"), ("w", "WATER"), ("h", "HILL")):
    surf = globals().get(var)
    if surf is not None:
        WORLD_OBJECT_SPRITES[sym] = surf

def draw_cell():
    """Сітка клітинок поверх усього вікна (сумісно з твоєю назвою)."""
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, WIDTH, BLOCK_SIZE):
            pg.draw.rect(window, "purple", (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

class TileWorld:
    """
    Двошарова карта фіксованого розміру:
      ground  : list[str] або list[list[str]] з символами '1'..'4' (типи трави)
      objects : list[str] або list[list[str]] з символами об'єктів ('.' — пусто)
    Жодної генерації — лише від наданих списків.
    """
    BLOCKING = {"t", "r", "w", "h"}
    EMPTY = "."
    OVERLAY = {"t"}

    def __init__(
        self,
        ground_map: list[str] | list[list[str]],
        object_map: list[str] | list[list[str]] | None = None,
        *,
        show_grid: bool = False,
    ) -> None:
        self.cols = WIDTH // BLOCK_SIZE
        self.rows = HEIGHT // BLOCK_SIZE
        self.ground = self._normalize_map(ground_map, default=self.EMPTY)
        self.objects = self._normalize_map(object_map or [], default=self.EMPTY)
        self.show_grid = show_grid

    # ----------------------- утиліти -----------------------
    def _normalize_map(self, src, default: str) -> list[str]:
        """Приводить в розмір rows x cols. Обрізає рядки та доповнює default."""
        out: list[str] = []
        if not src:
            return [default * self.cols for _ in range(self.rows)]
        for y in range(self.rows):
            if y < len(src):
                row = src[y]
                s = row if isinstance(row, str) else "".join(row)
            else:
                s = ""
            s = (s + default * self.cols)[: self.cols]
            out.append(s)
        return out

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def to_grid(self, px: int, py: int) -> tuple[int, int]:
        return px // BLOCK_SIZE, py // BLOCK_SIZE

    def to_screen(self, gx: int, gy: int) -> tuple[int, int]:
        return gx * BLOCK_SIZE, gy * BLOCK_SIZE

    def get_obj(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y):
            return self.EMPTY
        return self.objects[y][x]

    def set_obj(self, x: int, y: int, sym: str) -> None:
        if not self.in_bounds(x, y):
            return
        row = list(self.objects[y])
        row[x] = sym
        self.objects[y] = "".join(row)

    def clear_obj(self, x: int, y: int) -> None:
        self.set_obj(x, y, self.EMPTY)

    def is_blocking(self, x: int, y: int) -> bool:
        return self.get_obj(x, y) in self.BLOCKING

    # ----------------------- малювання ---------------------
    def draw_under(self, surface: pg.Surface) -> None:
        """Ґрунт + об'єкти, що не перекривають гравця."""
        bs = BLOCK_SIZE
        G = globals().get("WORLD_GROUND_SPRITES", {})  # {'1': Surface, ...}
        O = globals().get("WORLD_OBJECT_SPRITES", {})  # {'t': Surface, ...}

        # ґрунт
        for y, row in enumerate(self.ground):
            for x, ch in enumerate(row):
                surf = G.get(ch)
                if surf:
                    surface.blit(surf, (x * bs, y * bs))

        # об'єкти без оверлею
        for y, row in enumerate(self.objects):
            for x, ch in enumerate(row):
                if ch == self.EMPTY or ch in self.OVERLAY:
                    continue
                surf = O.get(ch)
                if surf:
                    surface.blit(surf, (x * bs, y * bs))
                else:
                    pad = max(1, bs // 8)
                    pg.draw.rect(surface, (0, 0, 0), (x * bs + pad, y * bs + pad, bs - 2 * pad, bs - 2 * pad))

        if self.show_grid:
            self.draw_grid(surface)

    def draw_over(self, surface: pg.Surface) -> None:
        """Об'єкти-оверлеї, що мають бути над гравцем."""
        bs = BLOCK_SIZE
        O = globals().get("WORLD_OBJECT_SPRITES", {})
        for y, row in enumerate(self.objects):
            for x, ch in enumerate(row):
                if ch not in self.OVERLAY:
                    continue
                surf = O.get(ch)
                if surf:
                    surface.blit(surf, (x * bs, y * bs))
                else:
                    pad = max(1, bs // 8)
                    pg.draw.rect(surface, (20, 20, 20), (x * bs + pad, y * bs + pad, bs - 2 * pad, bs - 2 * pad), 2)

    def draw(self, surface: pg.Surface) -> None:
        """Повний рендер: низ + верх."""
        self.draw_under(surface)
        self.draw_over(surface)

    def draw_grid(self, surface: pg.Surface, color=(40, 40, 40)) -> None:
        bs = BLOCK_SIZE
        for y in range(0, HEIGHT, bs):
            for x in range(0, WIDTH, bs):
                pg.draw.rect(surface, color, (x, y, bs, bs), 1)

    def get_ground(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y): return "1"
        return self.ground[y][x]