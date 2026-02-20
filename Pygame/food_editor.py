import pygame as pg
import settings
from .button import Button


class food_editor():
    def __init__(self, screen:pg.surface):
        self.screen = screen
        self.width, self.height = settings.Display_size

        #zone du graphe
        self.margin = 80
        self.graph_rect = pg.Rect(self.margin, self.margin, self.width - 2 * self.margin, self.height - 2 * self.margin)

        self.max_food = settings.Max_foood_quantity

        #generation initiale
        self.point = []
        self.generate_curve()

        self.dragging_index = None
        self.point_radius = 8

        #boutons
        self.v_button = Button(pg.Rect(self.width//2 - 120, self.height - 110, 240, 50), "Valider", self.screen)


    def generate_curve(self):
        self.point = []

        step_div = max(1, settings.Days_max - 1)
        step_x = self.graph_rect.width / step_div

        for i in range(settings.Days_max):
            x = self.graph_rect.x + i * step_x
            val = settings.Food_quantity[i] if i < len(settings.Food_quantity) else settings.Food_quantity_default
            y = self.value_to_y(val)
            self.point.append([x, y])



    def value_to_y(self, value):
        ratio = value / self.max_food
        return self.graph_rect.bottom - ratio * self.graph_rect.height

    def y_to_value(self, y):
        ratio = (self.graph_rect.bottom - y) / self.graph_rect.height
        return int(max(0, min(self.max_food, ratio * self.max_food)))

    def draw(self):
        self.screen.fill((240, 240, 240))

        # fond graphe
        pg.draw.rect(self.screen, (255,255,255), self.graph_rect)
        pg.draw.rect(self.screen, (0,0,0), self.graph_rect, 2)

        # ligne
        if len(self.point) > 1:
            pg.draw.lines(self.screen, (50,120,200), False, self.point, 2)

        # points
        for p in self.point:
            pg.draw.circle(self.screen, (200,50,50), (int(p[0]), int(p[1])), self.point_radius)

        # bouton
        self.v_button.draw(self.screen, pg.font.SysFont(settings.Button_font, settings.Button_font_size))



    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # clic sur bouton
            if self.v_button.rect.collidepoint(event.pos):
                self._apply_values()
                return "settings"

            # détection point
            for i, p in enumerate(self.point):
                if (mx - p[0])**2 + (my - p[1])**2 <= self.point_radius**2:
                    self.dragging_index = i
                    break

        if event.type == pg.MOUSEBUTTONUP:
            self.dragging_index = None

        if event.type == pg.MOUSEMOTION and self.dragging_index is not None:
            _, my = event.pos
            my = max(self.graph_rect.top, min(self.graph_rect.bottom, my))
            self.point[self.dragging_index][1] = my

    def _apply_values(self):
        values = [self.y_to_value(p[1]) for p in self.point]

        if len(values) < settings.Days_max:
            values += [values[-1] if values else settings.Food_quantity_default] * (settings.Days_max - len(values))
        elif len(values) > settings.Days_max:
            values = values[:settings.Days_max]

        settings.Food_quantity = values
