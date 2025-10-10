# game/effects.py
import random
import pygame as pg
from settings import BLOCK_SIZE

class Effects:
    def __init__(self):
        self.under: list[dict] = []  # сліди
        self.over: list[dict] = []   # частинки

    # ---- API ----
    def spawn_step(self, gx: int, gy: int, ground_ch: str, direction: str):
        self._add_footprint(gx, gy, direction)
        # для трави ('1'..'4') робимо легкий «пух»
        if ground_ch in ("1", "2", "3", "4"):
            self._add_grass_puff(gx, gy, direction)

    def update(self, dt: float):
        for bucket in (self.under, self.over):
            i = 0
            while i < len(bucket):
                p = bucket[i]
                p["life"] -= dt
                if p["life"] <= 0:
                    bucket.pop(i); continue
                # рух і згасання
                p["x"] += p.get("vx", 0) * dt
                p["y"] += p.get("vy", 0) * dt
                i += 1

    def draw_under(self, surface: pg.Surface):
        self._draw_bucket(surface, self.under)

    def draw_over(self, surface: pg.Surface):
        self._draw_bucket(surface, self.over)

    # ---- внутрішнє ----
    def _add_footprint(self, gx: int, gy: int, direction: str):
        # еліпс під лапою, орієнтуємо по напряму
        w = int(BLOCK_SIZE * 0.42)
        h = int(BLOCK_SIZE * 0.24)
        if direction in ("left", "right"):
            w, h = h, w
        px = gx * BLOCK_SIZE + BLOCK_SIZE // 2 - w // 2
        py = gy * BLOCK_SIZE + BLOCK_SIZE // 2 - h // 2
        self.under.append({
            "type": "ellipse",
            "x": px, "y": py, "w": w, "h": h,
            "color": (60, 80, 50, 160),   # темно-оливковий з альфою
            "life": 0.7
        })

    def _add_grass_puff(self, gx: int, gy: int, direction: str):
        cx = gx * BLOCK_SIZE + BLOCK_SIZE / 2
        cy = gy * BLOCK_SIZE + BLOCK_SIZE / 2
        n = 8
        for _ in range(n):
            ang = random.uniform(0, 3.1416 * 2)
            speed = random.uniform(30, 70)
            # легше зсув у напрямку кроку
            if direction == "right": vx_bias, vy_bias = 40, 0
            elif direction == "left": vx_bias, vy_bias = -40, 0
            elif direction == "down": vx_bias, vy_bias = 0, 40
            else: vx_bias, vy_bias = 0, -40
            vx = speed * 0.5 * pg.math.Vector2(1, 0).rotate_rad(ang).x + vx_bias
            vy = speed * 0.5 * pg.math.Vector2(0, 1).rotate_rad(ang).y + vy_bias
            r = random.randint(2, 4)
            # кольори: хакі/тан
            color = random.choice([(189,183,107,200), (210,180,140,200)])
            self.over.append({
                "type": "circle",
                "x": cx, "y": cy, "r": r,
                "vx": vx, "vy": vy,
                "color": color,
                "life": random.uniform(0.25, 0.45)
            })

    def _draw_bucket(self, surface: pg.Surface, bucket: list[dict]):
        for p in bucket:
            col = p["color"]
            # альфа від життя
            if len(col) == 4:
                a = int(col[3] * max(0.0, min(1.0, p["life"] / 0.7)))
                color = (col[0], col[1], col[2], a)
            else:
                color = (*col, 180)
            if p["type"] == "ellipse":
                s = pg.Surface((p["w"], p["h"]), pg.SRCALPHA)
                pg.draw.ellipse(s, color, (0, 0, p["w"], p["h"]))
                surface.blit(s, (int(p["x"]), int(p["y"])))
            elif p["type"] == "circle":
                d = p["r"] * 2
                s = pg.Surface((d, d), pg.SRCALPHA)
                pg.draw.circle(s, color, (p["r"], p["r"]), p["r"])
                surface.blit(s, (int(p["x"] - p["r"]), int(p["y"] - p["r"])))
