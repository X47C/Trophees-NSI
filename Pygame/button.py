import pygame as pg
from pygame import Rect

class Button:
    def __init__(self, rect:Rect, text:str, screen:pg.surface = None, *, editable:bool = False, max_length:int = 10, allow_decimal:bool = False, description:str = ''):
        self.rect = rect
        self.text = str(text)
        self.screen = screen

        self.editable = editable
        self.allow_decimal = allow_decimal
        self.max_length = max_length

        self.value = ""
        self.active = False

        #box de desciption
        self.description_font = pg.font.SysFont('Arial', 13)
        self.description_slices = self.description_slice(description)
        self.description_text = self.description_slices[0]
        self.description_box_size = (300, (self.description_font.get_linesize() + 5)* self.description_slices[1])
        self.description_box_color = (255, 255, 255)


    def draw(self, surf:pg.surface, font:pg.font, asset:str = None, bg:tuple = (30,144,255)):
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

    def get_number(self):
        if self.value == "":
            return None
        if self.allow_decimal:
            return float(self.value)
        return int(self.value)

    def set_value(self, v):
        if self.editable:
            self.value = str(v)[:self.max_length]


    def description_slice(self, text):
        step = 45
        lines = [text[i:i+step] for i in range(0, len(text), step)]
        return "\n".join(lines), len(lines)


    def description(self):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.description_text != '':
            desc_rect = pg.Rect((pos[0], pos[1] - self.description_box_size[1]), self.description_box_size)

            pg.draw.rect(self.screen, self.description_box_color, desc_rect, border_radius=8)
            pg.draw.rect(self.screen, (0,0,0), desc_rect, 2, border_radius=8)

            lines = self.description_text.splitlines()
            line_height = self.description_font.get_linesize()

            total_height = line_height * len(lines)
            start_y = desc_rect.top + (desc_rect.height - total_height) // 2

            for i, line in enumerate(lines):
                text_surface = self.description_font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.centerx = desc_rect.centerx
                text_rect.top = start_y + i * line_height
                self.screen.blit(text_surface, text_rect)
