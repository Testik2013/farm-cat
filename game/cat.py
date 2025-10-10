from settings import *

class Cat:
    width, height = BLOCK_SIZE, BLOCK_SIZE
    step = 1  # крок у клітинках

    def __init__(self, grid_x: int, grid_y: int):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = Rect(grid_x * BLOCK_SIZE, grid_y * BLOCK_SIZE, self.width, self.height)
        self.direction = "down"
        # трекаємо попередній стан клавіш для "один крок на натиск"
        self._prev = {
            K_w: False, K_a: False, K_s: False, K_d: False,
            K_UP: False, K_LEFT: False, K_DOWN: False, K_RIGHT: False,
        }

    # -------- рендер --------
    def reset(self) -> None:
        surf = CAT_SPRITES.get(self.direction, CAT_SPRITES["down"])
        window.blit(surf, self.rect)

    # -------- логіка руху --------
    def update(self, keys, world, effects=None) -> None:
        dx = dy = 0

        # пріоритет: D/A/S/W, потім стрілки
        if self._edge(keys, K_d) or self._edge(keys, K_RIGHT):
            self.direction = "right"; dx = self.step
        elif self._edge(keys, K_a) or self._edge(keys, K_LEFT):
            self.direction = "left";  dx = -self.step
        elif self._edge(keys, K_s) or self._edge(keys, K_DOWN):
            self.direction = "down";  dy = self.step
        elif self._edge(keys, K_w) or self._edge(keys, K_UP):
            self.direction = "up";    dy = -self.step

        if dx or dy:
            nx = self.grid_x + dx
            ny = self.grid_y + dy
            # межі карти
            if 0 <= nx < WIDTH // BLOCK_SIZE and 0 <= ny < HEIGHT // BLOCK_SIZE:
                # колізія по другому шару
                if not world.is_blocking(nx, ny):
                    self.grid_x, self.grid_y = nx, ny
                    self.rect.topleft = (nx * BLOCK_SIZE, ny * BLOCK_SIZE)
                    if effects:
                        gch = world.get_ground(nx, ny)
                        effects.spawn_step(nx, ny, gch, self.direction)
        # оновлюємо попередні стани
        for k in self._prev:
            self._prev[k] = keys[k]

    # -------- утиліти --------
    def _edge(self, keys, keycode) -> bool:
        """Повертає True лише на кадрі натискання."""
        return keys[keycode] and not self._prev[keycode]

    @property
    def cell(self) -> tuple[int, int]:
        return self.grid_x, self.grid_y

    def snap_to_grid(self) -> None:
        self.rect.topleft = (self.grid_x * BLOCK_SIZE, self.grid_y * BLOCK_SIZE)

    def teleport(self, gx: int, gy: int) -> None:
        """Миттєво переносить у клітинку без перевірок."""
        self.grid_x, self.grid_y = gx, gy
        self.snap_to_grid()
