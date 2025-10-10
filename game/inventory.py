# game/inventory.py
import pygame as pg
from settings import WIDTH, BLOCK_SIZE

class Inventory:
    def __init__(self, slots: list[dict], max_slots: int = 5):
        """
        slots: [{"code": "h", "name": "Hut", "count": 10}, ...]
        code => символ об'єкта у другому шарі world.objects
        """
        self.max_slots = max_slots
        self.slots: list[dict | None] = slots[:max_slots] + [None] * max(0, max_slots - len(slots))
        self.selected = 0
        self.font = pg.font.SysFont(None, 18)

        # UI
        self.slot_size = max(36, BLOCK_SIZE - 8)
        self.pad = 6
        self.margin = 10
        self.border = 2
        self.bg_color = (210, 180, 140)  # Tan, світло-коричневий
        self.slot_color = (189, 183, 107)  # DarkKhaki
        self.sel_color = (85, 107, 47)  # DarkOliveGreen
        self.text_color = (25, 25, 25)  # темний для цифр/літер

    # ---- вибір ----
    def select_index(self, idx: int) -> None:
        if 0 <= idx < self.max_slots:
            self.selected = idx

    def select_by_key(self, key_code: int) -> None:
        if pg.K_1 <= key_code <= pg.K_5:
            self.select_index(key_code - pg.K_1)

    # ---- доступ ----
    def get_selected(self) -> dict | None:
        return self.slots[self.selected]

    def consume_selected(self, n: int = 1) -> None:
        slot = self.get_selected()
        if not slot:
            return
        slot["count"] = max(0, slot.get("count", 0) - n)
        if slot["count"] == 0:
            self.slots[self.selected] = None

    def add_item(self, code: str, name: str = "", count: int = 1) -> None:
        # стекінг у перший слот з тим самим code, або в перший пустий
        for i, s in enumerate(self.slots):
            if s and s.get("code") == code:
                s["count"] = s.get("count", 0) + count
                return
        for i, s in enumerate(self.slots):
            if s is None:
                self.slots[i] = {"code": code, "name": name or code, "count": count}
                return

    # ---- рендер ----
    def draw(self, surface: pg.Surface, object_sprites: dict[str, pg.Surface] | None = None) -> None:
        n = self.max_slots
        S = self.slot_size
        total_w = n * S + (n - 1) * self.pad
        x0 = WIDTH - self.margin - total_w
        y0 = self.margin

        # фон панелі
        panel_rect = pg.Rect(x0 - self.margin // 2, y0 - self.margin // 2,
                             total_w + self.margin, S + self.margin)
        pg.draw.rect(surface, self.bg_color, panel_rect, border_radius=8)

        # слоти
        for i in range(n):
            x = x0 + i * (S + self.pad)
            r = pg.Rect(x, y0, S, S)
            pg.draw.rect(surface, self.slot_color, r, border_radius=6)

            # виділення активного
            if i == self.selected:
                pg.draw.rect(surface, self.sel_color, r, width=self.border, border_radius=6)

            slot = self.slots[i]
            if slot:
                code = slot.get("code")
                count = slot.get("count", 0)

                # іконка: беремо зі спрайтів другого шару, або літеру
                icon = None
                if object_sprites:
                    icon = object_sprites.get(code)
                if icon:
                    # масштаб у слот із полями
                    pad = 6
                    icon_scaled = pg.transform.smoothscale(icon, (S - 2 * pad, S - 2 * pad))
                    surface.blit(icon_scaled, (x + pad, y0 + pad))
                else:
                    # fallback: буква коду
                    letter = self.font.render(str(code), True, (230, 230, 230))
                    lx = x + (S - letter.get_width()) // 2
                    ly = y0 + (S - letter.get_height()) // 2
                    surface.blit(letter, (lx, ly))

                # лічильник
                txt = self.font.render(str(count), True, (240, 240, 240))
                surface.blit(txt, (x + S - txt.get_width() - 3, y0 + S - txt.get_height() - 2))
