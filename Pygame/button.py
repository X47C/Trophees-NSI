import pygame as pg
from pygame import Rect

class Button:
    def __init__(self, rect:Rect, text:str, screen:pg.surface = None, *, editable:bool = False, max_length:int = 10, allow_decimal:bool = False):
        self.rect = rect
        self.text = str(text)
        self.screen = screen

        self.editable = editable
        self.allow_decimal = allow_decimal
        self.max_length = max_length

        self.value = ""
        self.active = False


    def draw(self, surf:pg.surface, font, asset:str = None, bg:tuple = (30,144,255)):
        display_text = self.value if self.editable else self.text

        if asset:
            image = pg.image.load(asset).convert_alpha()
            surf.blit(image, (self.rect.x, self.rect.y))
            ts = font.render(display_text, True, (255,255,255))
            surf.blit(ts, (
                self.rect.x + (self.rect.w - ts.get_width()) // 2,
                self.rect.y + (self.rect.h - ts.get_height()) // 2
            ))
            return
        pg.draw.rect(surf, bg, self.rect, border_radius=8)
        pg.draw.rect(surf, (0,0,0), self.rect, 2, border_radius=8)

        if self.editable and display_text == "":
            ts = font.render(self.text, True, (200,200,200))
        else:
            ts = font.render(display_text, True, (255,255,255))

        surf.blit(ts, (
            self.rect.x + (self.rect.w - ts.get_width()) // 2,
            self.rect.y + (self.rect.h - ts.get_height()) // 2
        ))

        if self.editable and self.active:
            if (pg.time.get_ticks() // 500) % 2 == 0:
                text_w = ts.get_width()
                caret_x = self.rect.x + (self.rect.w - text_w) // 2 + text_w + 2
                caret_y = self.rect.y + (self.rect.h - ts.get_height()) // 2
                pg.draw.rect(surf, (255,255,255), (caret_x, caret_y, 2, ts.get_height()))

    def collide(self, pos:tuple):
        return self.rect.collidepoint(pos)

    def is_clicked(self, mouse_pos:tuple, button_pos:tuple):
        relative_pos = (mouse_pos[0] - button_pos[0], mouse_pos[1] - button_pos[1])
        return self.collide(relative_pos)

    def handle_event(self, event, offset=(0,0)):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            rel = (mx - offset[0], my - offset[1])

            if self.collide(rel):
                if self.editable:
                    self.active = True
                return True
            else:
                self.active = False

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.value = self.value[:-1]
                return True

            if event.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_ESCAPE):
                self.active = False
                return True

            ch = event.unicode
            if ch.isdigit() or (ch == '.' and self.allow_decimal and '.' not in self.value):
                if len(self.value) < self.max_length:
                    self.value += ch
                return True

        return False

    def get_text(self):
        return self.value if self.editable else self.text

    def get_number(self):
        if self.value == "":
            return None
        if self.allow_decimal:
            return float(self.value)
        return int(self.value)

    def set_value(self, v):
        if self.editable:
            self.value = str(v)[:self.max_length]

    def clear_value(self):
        self.value = ""
        self.active = False
