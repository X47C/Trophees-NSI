import pygame as pg
import math
import random
import settings
from .button import Button


PRESET_FUNCTIONS = {"Constante"  : "c", "Croissant"  : "c * (1 + j / D)", "Décroissant": "c * (1 - j / D)", "Sinusoide"  : "c + (m/4) * sin(2 * pi * j / D)", "Escalier"   : "c * (1 + int(j / (D/4)))", "Aléatoire"  : None}


class food_editor():
    """Éditeur qui permet de modifier la quantité de nourriture pour chaque jour de la simulation."""

    # couleurs de l'interface
    COL_BG = (28, 32, 42)
    COL_PANEL = (38, 44, 58)
    COL_GRAPH_BG = (22, 26, 36)
    COL_GRID = (50, 58, 76)
    COL_GRID_LABEL = (130, 140, 165)
    COL_CURVE = (80, 180, 255)
    COL_POINT = (255, 100, 80)
    COL_POINT_HL = (255, 200, 60)
    COL_AXIS = (180, 190, 210)
    COL_TEXT = (220, 225, 235)
    COL_TITLE = (255, 255, 255)
    COL_INPUT_BG = (50, 58, 76)
    COL_INPUT_ACT = (60, 90, 140)
    COL_INPUT_BD = (80, 120, 200)
    COL_INPUT_ERR = (200, 60, 60)
    COL_BTN = (55, 80, 130)
    COL_BTN_HL = (80, 120, 190)
    COL_BTN_VAL = (40, 130, 80)
    COL_BTN_VAL_HL = (60, 170, 100)

    def __init__(self, screen: pg.Surface):
        """Prépare tous les éléments de l'éditeur : graphe, boutons, champ de texte."""
        self.screen = screen
        self.width, self.height = settings.Display_size

        # surface sombre par dessus le fond
        self.overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.overlay.fill((10, 12, 20, 200))

        # pollices
        self.font_title = pg.font.SysFont("Arial", 22, bold = True)
        self.font_label = pg.font.SysFont("Arial", 14)
        self.font_axis = pg.font.SysFont("Arial", 12)
        self.font_btn = pg.font.SysFont("Arial", 14, bold = True)
        self.font_input = pg.font.SysFont("Consolas", 14)
        self.font_preset = pg.font.SysFont("Arial", 13)

        # marges autour du graphe
        self.left_margin = 100
        self.right_margin = 40
        self.top_margin = 80
        self.bottom_margin = 160

        self.graph_rect = pg.Rect(self.left_margin, self.top_margin, self.width - self.left_margin - self.right_margin, self.height - self.top_margin - self.bottom_margin)

        self.max_food = settings.Max_foood_quantity
        self.point_radius = 7

        # liste des points de la courbe
        self.point = []
        self.generate_curve()
        self.dragging_index = None
        self.hovered_index = None

        # zone de saisie des formules
        input_y = self.graph_rect.bottom + 18
        self.input_rect = pg.Rect(self.left_margin, input_y, 340, 34)
        self.input_active = False
        self.input_text = ""
        self.input_error = ""
        self.cursor_vis = True
        self.cursor_tick = 0

        btn_apply = pg.Rect(self.input_rect.right + 10, input_y, 90, 34)
        self.btn_apply = Button(btn_apply, "Appliquer", self.screen)

        # boutons pour les fonctions prédéfinies
        preset_names = list(PRESET_FUNCTIONS.keys())
        self.preset_rects = []
        bw = 108
        bh = 28
        gap = 8
        start_x = self.left_margin
        preset_y = input_y + 46
        for k, name in enumerate(preset_names):
            r = pg.Rect(start_x + k * (bw + gap), preset_y, bw, bh)
            self.preset_rects.append(r)

        # bouton de confirmation
        val_w = 160
        val_h = 40
        self.btn_validate = Button(pg.Rect(self.width // 2 - val_w // 2, self.height - val_h - 14, val_w, val_h), "Valider", self.screen)

    def value_to_y(self, value: float) -> float:
        """Transforme une quantité de nourriture en position Y sur l'écran."""
        ratio = value / self.max_food
        return self.graph_rect.bottom - ratio * self.graph_rect.height

    def y_to_value(self, y: float) -> int:
        """Transforme une position Y sur l'écran en quantité de nourriture."""
        ratio = (self.graph_rect.bottom - y) / self.graph_rect.height
        return int(max(0, min(self.max_food, ratio * self.max_food)))

    def day_to_x(self, i: int) -> float:
        """Transforme un numéro de jour en position X sur l'écran."""
        step_div = max(1, settings.Days_max - 1)
        return self.graph_rect.x + i * (self.graph_rect.width / step_div)

    def generate_curve(self):
        """Crée les points du graphe en lisant les valeurs enregistrées dans les settings."""
        self.point = []
        for i in range(settings.Days_max):
            x = self.day_to_x(i)
            if i < len(settings.Food_quantity):
                val = settings.Food_quantity[i]
            else:
                val = settings.Food_quantity_default
            self.point.append([x, self.value_to_y(val)])

    def apply_values(self):
        """Sauvegarde les positions actuelles des points dans les settings."""
        values = [self.y_to_value(p[1]) for p in self.point]
        n = settings.Days_max
        if len(values) < n:
            if values:
                default_val = values[-1]
            else:
                default_val = settings.Food_quantity_default
            values += [default_val] * (n - len(values))
        settings.Food_quantity = values[:n]

    def apply_formula(self, expr: str):
        """Calcule les valeurs de chaque jour à partir d'une formule mathématique et met à jour le graphe."""
        # variables disponibles dans la formule
        D = settings.Days_max
        m = self.max_food
        c = settings.Food_quantity_default
        safe_globals = {"__builtins__": {}, "j": 0, "D": D, "m": m, "c": c, "pi": math.pi, "sin": math.sin, "cos": math.cos, "abs": abs, "int": int, "round": round, "min": min, "max": max, "sqrt": math.sqrt, "floor": math.floor, "ceil": math.ceil}
        new_points = []
        try:
            for j in range(D):
                safe_globals["j"] = j
                val = eval(expr, safe_globals)
                val = max(0, min(m, float(val)))
                new_points.append([self.day_to_x(j), self.value_to_y(val)])
            self.point = new_points
            self.input_error = ""
        except Exception as e:
            self.input_error = f"Erreur : {e}"

    def apply_preset(self, name: str):
        """Applique un profil de courbe prédéfini (ex: croissant, sinusoïde, aléatoire...)."""
        expr = PRESET_FUNCTIONS[name]
        if expr is None:
            # en cas de valeurs aléatoires
            D = settings.Days_max
            m = self.max_food
            self.point = [[self.day_to_x(j), self.value_to_y(random.randint(0, m))]for j in range(D)]
            self.input_error = ""
        else:
            self.input_text = expr
            self.apply_formula(expr)

    def draw(self):
        """Dessine tout l'éditeur sur l'écran."""
        self.screen.fill(self.COL_BG)
        self.draw_panel()
        self.draw_graph()
        self.draw_controls()

    def draw_panel(self):
        """Dessine le fond, le titre et les labels des axes."""
        panel = pg.Surface((self.width - 40, self.height - 20), pg.SRCALPHA)
        panel.fill((30, 36, 52, 210))
        self.screen.blit(panel, (20, 10))

        # titre en haut au centre
        title = self.font_title.render("Éditeur de nourriture par jour", True, self.COL_TITLE)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 26))

        # légende axe y
        lbl_y = self.font_label.render("Quantité", True, self.COL_TEXT)
        lbl_rot = pg.transform.rotate(lbl_y, 90)
        self.screen.blit(lbl_rot, (18, self.graph_rect.centery - lbl_rot.get_height() // 2))

        # légende axe x
        lbl_x = self.font_label.render("Jours", True, self.COL_TEXT)
        self.screen.blit(lbl_x, (self.graph_rect.centerx - lbl_x.get_width() // 2, self.graph_rect.bottom + 6))

    def draw_graph(self):
        """Dessine le graphe : grille, courbe et points déplaçables."""
        gr = self.graph_rect

        # fond du graphe
        pg.draw.rect(self.screen, self.COL_GRAPH_BG, gr, border_radius=6)

        # lignes horizontales de la grille
        grid_steps = 5
        for k in range(grid_steps + 1):
            val = self.max_food * k / grid_steps
            y = self.value_to_y(val)
            pg.draw.line(self.screen, self.COL_GRID, (gr.left, int(y)), (gr.right, int(y)), 1)
            lbl = self.font_axis.render(str(int(val)), True, self.COL_GRID_LABEL)
            self.screen.blit(lbl, (gr.left - lbl.get_width() - 6, int(y) - lbl.get_height() // 2))

        # lignes verticales et étiquettes des jours
        D = settings.Days_max
        step_label = max(1, D // 10)
        for j in range(D):
            x = int(self.day_to_x(j))
            pg.draw.line(self.screen, self.COL_GRID, (x, gr.top), (x, gr.bottom), 1)
            if j % step_label == 0 or j == D - 1:
                lbl = self.font_axis.render(str(j + 1), True, self.COL_GRID_LABEL)
                self.screen.blit(lbl, (x - lbl.get_width() // 2, gr.bottom + 6))

        # bordure du graphe
        pg.draw.rect(self.screen, self.COL_AXIS, gr, 2, border_radius=6)

        # dessin de la courbe
        if len(self.point) > 1:
            pts = [(int(p[0]), int(p[1])) for p in self.point]

            # zone remplie sous la courbe
            fill_pts = [(gr.left, gr.bottom)] + pts + [(gr.right, gr.bottom)]
            fill_surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
            pg.draw.polygon(fill_surf, (*self.COL_CURVE, 35), fill_pts)
            self.screen.blit(fill_surf, (0, 0))

            pg.draw.lines(self.screen, self.COL_CURVE, False, pts, 2)

        # dessin de chaque point
        for i, p in enumerate(self.point):
            px = int(p[0])
            py = int(p[1])
            is_hover = (i == self.hovered_index)
            is_drag = (i == self.dragging_index)
            if is_hover or is_drag:
                col = self.COL_POINT_HL
            else:
                col = self.COL_POINT
            if is_drag:
                r = self.point_radius + 2
            elif is_hover:
                r = self.point_radius + 1
            else:
                r = self.point_radius

            # ombre puis cercle principal
            pg.draw.circle(self.screen, (20, 20, 30), (px + 1, py + 1), r)
            pg.draw.circle(self.screen, col, (px, py), r)
            pg.draw.circle(self.screen, (255, 255, 255), (px, py), r, 1)

            # survol ou drag
            if is_hover or is_drag:
                val = self.y_to_value(p[1])
                tip = self.font_axis.render(f"J{i+1}: {val}", True, self.COL_TITLE)
                tip_bg = pg.Rect(px - tip.get_width() // 2 - 4, py - 28, tip.get_width() + 8, tip.get_height() + 4)
                pg.draw.rect(self.screen, (40, 50, 70), tip_bg, border_radius=4)
                pg.draw.rect(self.screen, self.COL_CURVE, tip_bg, 1, border_radius=4)
                self.screen.blit(tip, (tip_bg.x + 4, tip_bg.y + 2))

    def draw_controls(self):
        """Dessine les boutons, le champ de saisie de formule et l'aide en bas de l'écran."""
        # label au dessus du champ de saisie
        lbl = self.font_label.render("Formule :", True, self.COL_TEXT)
        self.screen.blit(lbl, (self.left_margin, self.input_rect.y - lbl.get_height() - 4))

        # couleurs du champ selon l'état
        if self.input_error:
            bd_col = self.COL_INPUT_ERR
        elif self.input_active:
            bd_col = self.COL_INPUT_BD
        else:
            bd_col = (80, 90, 110)
        if self.input_active:
            bg_col = self.COL_INPUT_ACT
        else:
            bg_col = self.COL_INPUT_BG

        pg.draw.rect(self.screen, bg_col, self.input_rect, border_radius=6)
        pg.draw.rect(self.screen, bd_col, self.input_rect, 2, border_radius=6)

        # texte dans le champ ou placeholder
        if self.input_text:
            display = self.input_text
            col_txt = self.COL_TEXT
        else:
            display = "ex: c * sin(pi * j / D) + c"
            col_txt = (100, 110, 130)

        txt_surf = self.font_input.render(display, True, col_txt)
        clip = pg.Rect(self.input_rect.x + 6, self.input_rect.y, self.input_rect.width - 12, self.input_rect.height)
        self.screen.set_clip(clip)
        self.screen.blit(txt_surf, (self.input_rect.x + 6, self.input_rect.y + (self.input_rect.height - txt_surf.get_height()) // 2))
        self.screen.set_clip(None)

        # curseur clignotant
        if self.input_active and self.cursor_vis:
            cx = self.input_rect.x + 8 + txt_surf.get_width()
            cy = self.input_rect.y + 6
            pg.draw.line(self.screen, self.COL_TEXT, (cx, cy), (cx, self.input_rect.bottom - 6), 2)

        # message d'erreur si besoin
        if self.input_error:
            err = self.font_axis.render(self.input_error, True, self.COL_INPUT_ERR)
            self.screen.blit(err, (self.input_rect.x, self.input_rect.bottom + 2))

        # bouton appliquer
        mx, my = pg.mouse.get_pos()
        if self.btn_apply.rect.collidepoint(mx, my):
            apply_col = self.COL_BTN_HL
        else:
            apply_col = self.COL_BTN
        pg.draw.rect(self.screen, apply_col, self.btn_apply.rect, border_radius=6)
        pg.draw.rect(self.screen, (120, 160, 230), self.btn_apply.rect, 1, border_radius=6)
        lbl_a = self.font_btn.render("Appliquer", True, self.COL_TITLE)
        self.screen.blit(lbl_a, (self.btn_apply.rect.x + (self.btn_apply.rect.width - lbl_a.get_width()) // 2,self.btn_apply.rect.y + (self.btn_apply.rect.height - lbl_a.get_height()) // 2))

        # boutons des fonctions prédéfinies
        preset_names = list(PRESET_FUNCTIONS.keys())
        for k, (name, r) in enumerate(zip(preset_names, self.preset_rects)):
            if r.collidepoint(mx, my):
                bg = self.COL_BTN_HL
            else:
                bg = self.COL_BTN
            pg.draw.rect(self.screen, bg, r, border_radius=5)
            pg.draw.rect(self.screen, (100, 130, 200), r, 1, border_radius=5)
            lbl_p = self.font_preset.render(name, True, self.COL_TITLE)
            self.screen.blit(lbl_p, (r.x + (r.width - lbl_p.get_width()) // 2, r.y + (r.height - lbl_p.get_height()) // 2))

        # petite aide sur les variables disponibles
        hint = ("Variables : j = jour (0-based)  |  D = nb jours  |  "
                "m = max nourriture  |  c = valeur par défaut  |  "
                "Fonctions : sin cos abs int sqrt min max")
        hint_surf = self.font_axis.render(hint, True, (90, 100, 130))
        self.screen.blit(hint_surf, (self.left_margin, self.preset_rects[0].bottom + 6))

        # bouton valider en bas au centre
        if self.btn_validate.rect.collidepoint(mx, my):
            val_col = self.COL_BTN_VAL_HL
        else:
            val_col = self.COL_BTN_VAL
        pg.draw.rect(self.screen, val_col, self.btn_validate.rect, border_radius=8)
        pg.draw.rect(self.screen, (80, 200, 120), self.btn_validate.rect, 1, border_radius=8)
        lbl_v = self.font_btn.render("Valider", True, self.COL_TITLE)
        self.screen.blit(lbl_v, (self.btn_validate.rect.x + (self.btn_validate.rect.width - lbl_v.get_width()) // 2, self.btn_validate.rect.y + (self.btn_validate.rect.height - lbl_v.get_height()) // 2))

    def handle_event(self, event):
        """Gère les clics, le drag des points et la saisie au clavier. Retourne 'settings' quand on clique sur Valider."""
        #fait clignoter le curseur à chaque appel
        self.cursor_tick += 1
        if self.cursor_tick > 30:
            self.cursor_tick = 0
            self.cursor_vis = not self.cursor_vis

        mx, my = pg.mouse.get_pos()

        #cherche si la souris survole un point
        self.hovered_index = None
        if self.dragging_index is None:
            for i, p in enumerate(self.point):
                if (mx - p[0])**2 + (my - p[1])**2 <= (self.point_radius + 4)**2:
                    self.hovered_index = i
                    break

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            # clic sur valider
            if self.btn_validate.rect.collidepoint(mx, my):
                self.apply_values()
                return "settings"

            # clic sur appliquer
            if self.btn_apply.rect.collidepoint(mx, my):
                if self.input_text.strip():
                    self.apply_formula(self.input_text.strip())
                return None

            # clic sur un preset
            preset_names = list(PRESET_FUNCTIONS.keys())
            for name, r in zip(preset_names, self.preset_rects):
                if r.collidepoint(mx, my):
                    self.apply_preset(name)
                    return None

            # active ou désactive le champ de saisie
            if self.input_rect.collidepoint(mx, my):
                self.input_active = True
                self.cursor_vis = True
                self.cursor_tick = 0
            else:
                self.input_active = False

            # commence à drag un point
            for i, p in enumerate(self.point):
                if (mx - p[0])**2 + (my - p[1])**2 <= (self.point_radius + 4)**2:
                    self.dragging_index = i
                    self.input_active = False
                    break

        if event.type == pg.MOUSEBUTTONUP:
            self.dragging_index = None

        if event.type == pg.MOUSEMOTION and self.dragging_index is not None:
            _, my_pos = event.pos
            my_pos = max(self.graph_rect.top, min(self.graph_rect.bottom, my_pos))
            self.point[self.dragging_index][1] = my_pos

        # gestion du clavier dans le champ de saisie
        if event.type == pg.KEYDOWN and self.input_active:
            if event.key == pg.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                self.input_error = ""
            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                if self.input_text.strip():
                    self.apply_formula(self.input_text.strip())
                self.input_active = False
            elif event.key == pg.K_ESCAPE:
                self.input_active = False
            else:
                ch = event.unicode
                if ch and ch.isprintable():
                    self.input_text += ch
                    self.input_error = ""

        return None