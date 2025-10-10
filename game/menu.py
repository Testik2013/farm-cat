# game/menu.py
import pygame as pg
from settings import WIDTH, HEIGHT

TAN         = (210, 180, 140)  # фон
DARK_KHAKI  = (189, 183, 107)  # панель / кнопки
OLIVE_BORDER= (85, 107, 47)    # акцент
TEXT_DARK   = (25, 25, 25)

class Menu:
    def __init__(self, options: list[tuple[str, str]], title: str = "CAT ADVENTURE"):
        """
        options: list of (id, label), напр. [("continue","Продовжити"), ("new","Нова гра"), ...]
        """
        self.options = options
        self.selected = 0
        self.hover = -1

        pg.font.init()
        self.f_title = pg.font.SysFont(None, 64)
        self.f_btn   = pg.font.SysFont(None, 36)
        self.f_key   = pg.font.SysFont(None, 22)

        # геометрія
        self.panel_w = min(720, int(WIDTH * 0.75))
        self.panel_h = min(520, int(HEIGHT * 0.8))
        self.panel_r = 16
        self.btn_w   = int(self.panel_w * 0.7)
        self.btn_h   = 56
        self.btn_gap = 14

        self.panel_rect = pg.Rect(
            (WIDTH - self.panel_w)//2,
            (HEIGHT - self.panel_h)//2,
            self.panel_w, self.panel_h
        )
        self._compute_buttons()

        # легкий затемнювач заднього фону
        self.backdrop = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.backdrop.fill((0, 0, 0, 60))

    def _compute_buttons(self):
        top = self.panel_rect.y + 140
        left = self.panel_rect.x + (self.panel_w - self.btn_w)//2
        self.btn_rects = []
        for _ in self.options:
            r = pg.Rect(left, top, self.btn_w, self.btn_h)
            self.btn_rects.append(r)
            top += self.btn_h + self.btn_gap

    # ------ події ------
    def handle_event(self, e) -> str | None:
        if e.type == pg.KEYDOWN:
            if e.key in (pg.K_UP, pg.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif e.key in (pg.K_DOWN, pg.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif e.key in (pg.K_RETURN, pg.K_SPACE):
                return self.options[self.selected][0]
            elif pg.K_1 <= e.key <= pg.K_9:
                idx = e.key - pg.K_1
                if 0 <= idx < len(self.options):
                    self.selected = idx
                    return self.options[idx][0]

        elif e.type == pg.MOUSEMOTION:
            self.hover = -1
            for i, r in enumerate(self.btn_rects):
                if r.collidepoint(e.pos):
                    self.hover = i
                    break
        elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            for i, r in enumerate(self.btn_rects):
                if r.collidepoint(e.pos):
                    self.selected = i
                    return self.options[i][0]
        return None

    # ------ рендер ------
    def draw(self, surface: pg.Surface):
        surface.blit(self.backdrop, (0, 0))

        # панель
        pg.draw.rect(surface, TAN, self.panel_rect, border_radius=self.panel_r)
        inner = self.panel_rect.inflate(-16, -16)
        pg.draw.rect(surface, DARK_KHAKI, inner, border_radius=self.panel_r)

        # заголовок
        t = self.f_title.render("CAT ADVENTURE", True, TEXT_DARK)
        surface.blit(t, (self.panel_rect.centerx - t.get_width()//2, self.panel_rect.y + 40))

        # кнопки
        for i, (opt_id, label) in enumerate(self.options):
            r = self.btn_rects[i]
            # тіло кнопки
            pg.draw.rect(surface, TAN, r, border_radius=10)
            # бордер: активний або hover
            if i == self.selected or i == self.hover:
                pg.draw.rect(surface, OLIVE_BORDER, r, width=3, border_radius=10)
            else:
                pg.draw.rect(surface, (120, 120, 90), r, width=2, border_radius=10)

            # текст
            txt = self.f_btn.render(label, True, TEXT_DARK)
            surface.blit(txt, (r.centerx - txt.get_width()//2, r.centery - txt.get_height()//2))

            # підказка клавіші 1..5
            if i < 9:
                key_lbl = self.f_key.render(str(i + 1), True, TEXT_DARK)
                surface.blit(key_lbl, (r.x + 10, r.y + (r.height - key_lbl.get_height())//2))
