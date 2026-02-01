# Ensemble des methodes servant a faire marcher pygame, on a before game avec les menu et les dispositions pour créer une partie
import pygame as pg
from Pygame.button import Button
from pygame import Rect
import settings
import matplotlib as plt
plt.use("Agg")  # backend sans fenêtre
import pylab
import matplotlib.backends.backend_agg as agg

class Before_Game:
    """
    permet de gérer l'écran avant le lancement de la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran avant le lancement de la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 - 40, 220, 80),'Exit', self.screen)
        self.Button_Start = Button(Rect(self.width // 2 - 110, self.height // 2 - 130, 220, 80),'Start', self.screen)
        self.Button_credits = Button(Rect(self.width // 2 - 110, self.height // 2 + 50, 220, 80),'Credits', self.screen) 
        self.Button_credits_exit = Button(Rect(self.width // 2 - 65, self.height // 2 + 130, 130, 50),'Back', self.screen)
        
        self.bg_asset = pg.image.load('assets/before-game-background.png')

        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def draw(self):
        """
        Dessine l'écran avant le lancement de la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_exit.draw(self.screen, self.Button_font, 'assets/button-exit.png')
        self.Button_Start.draw(self.screen, self.Button_font, 'assets/button-start.png')
        self.Button_credits.draw(self.screen, self.Button_font, 'assets/button-credits.png')

    def handle_event(self, event):
        """
        Gère les événements de l'écran avant le lancement de la partie
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.Button_exit.rect.collidepoint(event.pos):  
                    return 'exit'
                if self.Button_Start.rect.collidepoint(event.pos):
                    return 'start'
                if self.Button_credits.rect.collidepoint(event.pos):
                    return 'credits'
                if self.Button_credits_exit.rect.collidepoint(event.pos):
                    return 'home'
                
    def credits(self):
        """
        Affiche les crédits du jeu
        A modifier avec une image quand on en aura une
        """
        pg.draw.rect(self.screen, (255,255,255), (100,100, self.width - 200, self.height - 200))
        self.Button_credits_exit.draw(self.screen, self.Button_font)
        for i in range(len(settings.Credits_Text)):
            self.screen.blit(pg.font.SysFont(settings.Credits_font, settings.Credits_font_size).render(settings.Credits_Text[i], True, (0,0,0)), (self.width // 2 - 150, 130 + 80 * i))
    



class Settings:
    """
    """

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = settings.Display_size

        # fonts
        self.font_btn = pg.font.SysFont(settings.Button_font, settings.Button_font_size)
        self.font_lbl = pg.font.SysFont(settings.Button_label_font, settings.Button_label_font_size)
        

        # geometry
        settings.PostG_PADDING = 20
        self.gap = 18
        self.btn_h = 44
        self.small_w = 48
        self.label_gap = 6

        # couleur de fond pour le bouton numéroté sélectionné (modifiable)
        # ex : (120, 200, 140) = vert doux ; remplace par ce que tu veux
        self.pop_selected_bg = (120, 200, 140)

        # Espaces ajustables
        self.pop_manage_top_space = 60
        self.pop_manage_bottom_space = 48

        # selected population index
        self.selected_pop = 0

        # construction initiale de l'UI
        self._build_general_controls()
        self._build_pop_management_buttons()
        self._build_pop_controls()
        self._build_bottom_buttons()

    def update_layout(self):
        sel = self.selected_pop
        self._build_general_controls()
        self._build_pop_management_buttons()
        self._build_pop_controls()
        self._build_bottom_buttons()
        self.selected_pop = sel
        self._refresh_general_display()
        self._refresh_pop_display()

    def _build_general_controls(self):
        total_w = self.width - settings.PostG_PADDING * 2
        col_w = (total_w - self.gap) // 2
        val_w = col_w - self.small_w * 2 - 12

        top_y = settings.PostG_PADDING

        # food - left
        x0 = settings.PostG_PADDING
        lbl_y = top_y
        btn_y = lbl_y + self.font_lbl.get_height() + self.label_gap
        self.general_food = {
            "label": "Quantité de nourriture",
            "minus": Button(Rect(x0, btn_y, self.small_w, self.btn_h), "-", self.screen),
            "value": Button(Rect(x0 + self.small_w + 6, btn_y, val_w, self.btn_h), str(settings.Food_quantity), self.screen),
            "plus": Button(Rect(x0 + self.small_w + 6 + val_w + 6, btn_y, self.small_w, self.btn_h), "+", self.screen),
            "lbl_pos": (x0 + (col_w // 2), lbl_y)
        }

        # days - right
        x1 = settings.PostG_PADDING + col_w + self.gap
        lbl_y = top_y
        btn_y = lbl_y + self.font_lbl.get_height() + self.label_gap
        self.general_days = {
            "label": "Nombre de jours de la simulation",
            "minus": Button(Rect(x1, btn_y, self.small_w, self.btn_h), "-", self.screen),
            "value": Button(Rect(x1 + self.small_w + 6, btn_y, val_w, self.btn_h), str(settings.Days_max), self.screen),
            "plus": Button(Rect(x1 + self.small_w + 6 + val_w + 6, btn_y, self.small_w, self.btn_h), "+", self.screen),
            "lbl_pos": (x1 + (col_w // 2), lbl_y)
        }

        base_line = btn_y + self.btn_h
        self.pop_manage_y = base_line + self.pop_manage_top_space
        self.pop_controls_start_y = self.pop_manage_y + 36 + self.pop_manage_bottom_space

    def _build_pop_management_buttons(self):
        y = self.pop_manage_y

        # boutons + / -
        self.btn_add_pop = Button(Rect(settings.PostG_PADDING, y, 110, 36), "+ Pop", self.screen)
        self.btn_rem_pop = Button(Rect(settings.PostG_PADDING + 120, y, 110, 36), "- Pop", self.screen)

        # petits boutons numérotés alignés sur la même ligne
        self.pop_number_buttons = []
        x = settings.PostG_PADDING + 260
        for i in range(len(settings.POPULATIONS)):
            rect = Rect(x, y, 40, 36)
            self.pop_number_buttons.append((rect, i))
            x += 46

    def _build_pop_controls(self):
        if len(settings.POPULATIONS) == 0:
            if hasattr(settings, 'DEFAULT_POP'):
                settings.POPULATIONS.append(settings.DEFAULT_POP.copy())
            else:
                settings.POPULATIONS.append({
                    "name": "Population 1", "life": 50, "color": "white", "quantity": 10,
                    "speed_variation": 15, "size_variation": 15, "view_variation": 15,
                    "view": 15, "speed": 3, "size": 3
                })

        self.selected_pop = max(0, min(self.selected_pop, len(settings.POPULATIONS) - 1))
        pop = settings.POPULATIONS[self.selected_pop]

        labels = [
            ("Durée de vie des créatures", "life"),
            ("Couleur des créatures", "color"),
            ("Quantité de créatures", "quantity"),
            ("Taux de variation de la vitesse", "speed_variation"),
            ("Taux de variation de la taille", "size_variation"),
            ("Taux de variation de la vue", "view_variation"),
            ("Taille de vue au départ", "view"),
            ("Vitesse de départ", "speed"),
            ("Taille de départ", "size"),
        ]

        total_w = self.width - 2 * settings.PostG_PADDING
        col_w = (total_w - 2 * self.gap) // 3
        val_w = col_w - self.small_w * 2 - 12

        self.pop_controls = {}
        for idx, (label, key) in enumerate(labels):
            col = idx % 3
            row = idx // 3
            x = settings.PostG_PADDING + col * (col_w + self.gap)
            y_label = self.pop_controls_start_y + row * (self.font_lbl.get_height() + self.label_gap + self.btn_h + 18)
            y_btn = y_label + self.font_lbl.get_height() + self.label_gap

            cur_val = pop.get(key, "")
            if isinstance(cur_val, bool):
                display = '1' if cur_val else '0'
            else:
                display = str(cur_val)

            minus = Button(Rect(x, y_btn, self.small_w, self.btn_h), "-", self.screen)
            value = Button(Rect(x + self.small_w + 6, y_btn, val_w, self.btn_h), display, self.screen)
            plus = Button(Rect(x + self.small_w + 6 + val_w + 6, y_btn, self.small_w, self.btn_h), "+", self.screen)

            center_x = x + (col_w // 2)
            self.pop_controls[key] = {
                "label": label,
                "label_pos": (center_x, y_label),
                "minus": minus,
                "value": value,
                "plus": plus
            }

    def _build_bottom_buttons(self):
        y = self.height - (self.btn_h + 20)
        w = 220
        gap = 24
        x = (self.width - (2 * w + gap)) // 2
        self.btn_start = Button(Rect(x, y, w, self.btn_h), "Start", self.screen)
        self.btn_back = Button(Rect(x + w + gap, y, w, self.btn_h), "Back", self.screen)

    def draw(self):
        self.screen.fill(settings.UI_BG_COLOR if hasattr(settings, 'UI_BG_COLOR') else (200, 200, 200))
        pg.draw.rect(self.screen, settings.UI_PANEL_COLOR if hasattr(settings, 'UI_PANEL_COLOR') else (240,240,240),
                     (0, 0, self.width, self.height))

        # general labels + buttons
        for g in (self.general_food, self.general_days):
            label_surf = self.font_lbl.render(g["label"], True, (0, 0, 0))
            cx, ly = g["lbl_pos"]
            lx = int(cx - label_surf.get_width() // 2)
            self.screen.blit(label_surf, (lx, ly))
            g["minus"].draw(self.screen, self.font_btn)
            g["value"].draw(self.screen, self.font_btn)
            g["plus"].draw(self.screen, self.font_btn)

        # draw pop manage line (add/remove + numbers)
        self.btn_add_pop.draw(self.screen, self.font_btn)
        self.btn_rem_pop.draw(self.screen, self.font_btn)

        for rect, i in self.pop_number_buttons:
            if i == self.selected_pop:
                highlight_color = self.pop_selected_bg
                pg.draw.rect(self.screen, highlight_color, (rect.x, rect.y, rect.width, rect.height))
                txt = self.font_btn.render(str(i+1), True, (255, 255, 255))
                tx = rect.x + (rect.width - txt.get_width()) // 2
                ty = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx, ty))
            else:
                b = Button(Rect(rect.x, rect.y, rect.width, rect.height), str(i+1), self.screen)
                b.draw(self.screen, self.font_btn)

        # draw pop controls grid (labels centered)
        for key, c in self.pop_controls.items():
            label_surf = self.font_lbl.render(c["label"], True, (0,0,0))
            cx, ly = c["label_pos"]
            lx = int(cx - label_surf.get_width() // 2)
            self.screen.blit(label_surf, (lx, ly))
            c["minus"].draw(self.screen, self.font_btn)
            c["value"].draw(self.screen, self.font_btn)
            c["plus"].draw(self.screen, self.font_btn)

        # bottom buttons
        self.btn_start.draw(self.screen, self.font_btn)
        self.btn_back.draw(self.screen, self.font_btn)

    def _refresh_general_display(self):
        self.general_food["value"].text = str(settings.Food_quantity)
        self.general_days["value"].text = str(settings.Days_max)

    def _refresh_pop_display(self):
        if len(settings.POPULATIONS) == 0:
            return
        pop = settings.POPULATIONS[self.selected_pop]
        for key, c in self.pop_controls.items():
            v = pop.get(key, "")
            if isinstance(v, bool):
                c["value"].text = '1' if v else '0'
            else:
                c["value"].text = str(v)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # bottom
            if self.btn_start.rect.collidepoint(event.pos):
                return 'start'
            if self.btn_back.rect.collidepoint(event.pos):
                return 'back'

            mx, my = event.pos

            # general controls
            for name, g in (("Food_quantity", self.general_food), ("Simulation_duration", self.general_days)):
                if g["minus"].rect.collidepoint((mx,my)):
                    if name == "Food_quantity":
                        settings.Food_quantity = max(0, settings.Food_quantity - 1)
                    else:
                        settings.Days_max = max(1, settings.Days_max - 1)
                    self._refresh_general_display()
                    return None
                if g["plus"].rect.collidepoint((mx,my)):
                    if name == "Food_quantity":
                        settings.Food_quantity = min(settings.Max_foood_quantity, settings.Food_quantity + 1)
                    else:
                        settings.Days_max = min(settings.Max_days_max, settings.Days_max + 1)
                    self._refresh_general_display()
                    return None

            # add / remove pop
            if self.btn_add_pop.rect.collidepoint((mx,my)):
                if len(settings.POPULATIONS) < settings.POPULATION_MAX:
                    new_idx = len(settings.POPULATIONS) + 1
                    base = settings.DEFAULT_POP.copy() if hasattr(settings, 'DEFAULT_POP') else {
                        "name": f"Population {new_idx}",
                        "life": 50, "color": "white", "quantity": 10,
                        "speed_variation": 15, "size_variation": 15, "view_variation": 15,
                        "view": 15, "speed": 3, "size": 3
                    }
                    base["name"] = f"Population {new_idx}"
                    settings.POPULATIONS.append(base)
                    self.selected_pop = len(settings.POPULATIONS) - 1
                    self._build_pop_management_buttons()
                    self._build_pop_controls()
                    self._refresh_pop_display()
                return None

            if self.btn_rem_pop.rect.collidepoint((mx,my)):
                if len(settings.POPULATIONS) > settings.POPULATION_MIN:
                    settings.POPULATIONS.pop(self.selected_pop)
                    self.selected_pop = max(0, min(self.selected_pop, len(settings.POPULATIONS)-1))
                    self._build_pop_management_buttons()
                    self._build_pop_controls()
                    self._refresh_pop_display()
                return None

            for rect, idx in self.pop_number_buttons:
                if rect.collidepoint((mx,my)):
                    self.selected_pop = idx
                    self._build_pop_controls()
                    self._refresh_pop_display()
                    return None

            # per-population controls yea yea I'm english c'est une catastrophe la motié des commentaires sont dans une langue et l'autre motiée dasn une autre
            if len(settings.POPULATIONS) == 0:
                return None
            pop = settings.POPULATIONS[self.selected_pop]
            for key, c in self.pop_controls.items():
                if c["minus"].rect.collidepoint((mx,my)):
                    cur = pop.get(key)
                    if key == "color":
                        opts = getattr(settings, 'Color_options', [])
                        if opts:
                            try:
                                i = opts.index(cur)
                            except ValueError:
                                i = 0
                            pop["color"] = opts[(i - 1) % len(opts)]
                    elif isinstance(cur, int):
                        pop[key] = max(0, cur - 1)
                    self._refresh_pop_display()
                    return None
                
                if c["plus"].rect.collidepoint((mx,my)):
                    cur = pop.get(key)
                    match key:
                        case 'color':
                            opts = getattr(settings, 'Color_options', [])
                            if opts:
                                try:
                                    i = opts.index(cur)
                                except ValueError:
                                    i = 0
                                pop["color"] = opts[(i + 1) % len(opts)]
                        case 'life':
                            pop[key] = min(cur + 1, settings.Max_life)
                        case 'quantity':
                            pop[key] = min(cur + 1, settings.Max_quantity)
                        case 'size':
                            pop[key] = min(cur + 1, settings.Max_caracteristic)
                        case 'speed':
                            pop[key] = min(cur + 1, settings.Max_caracteristic)
                        case 'view':
                            pop[key] = min(cur + 1, settings.Max_caracteristic)
                        case 'size_variation':
                            pop[key] = min(cur + 1, 100) #c'est des pourcent donc max 100 je crois je sais meme pas si ca a un sens 100
                        case 'view_variation':
                            pop[key] = min(cur + 1, 100) #c'est des pourcent donc max 100 je crois je sais meme pas si ca a un sens 100
                        case 'speed_variation':
                            pop[key] = min(cur + 1, 100) #c'est des pourcent donc max 100 je crois je sais meme pas si ca a un sens 100
                    self._refresh_pop_display()
                    return None

        return None

        
            

class In_Game:
    """
    permet de gérer l'écran pendant la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran pendant la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen
        
        # self.bg_asset = pg.image.load('assets/bg_in_game.png')
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((34, 139, 34))

        self.continue_button = Button(Rect(self.width - self.width // 17, self.height // 60, 90, 40), 'End', self.screen)
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

    def draw(self, l_creatures, screen):
        """
        Dessine l'écran pendant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.continue_button.draw(self.screen, self.Button_font)
        #affiche les cratures
        for a in l_creatures:
            for c in a:
                c.draw(screen)
        for f in settings.food_list:
            f.draw(screen)

    def handle_event(self, event):
        """
        Gère les événements de l'écran pendant la partie
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1 :        
            if self.continue_button.rect.collidepoint(event.pos):
                return 'end'
                



class Post_Game:
    """
    écran après la partie
    avec scrollbar + graphiques matplotlib intégrés
    """

    def __init__(self, screen, current_day):
        self.width, self.height = settings.Display_size
        self.screen = screen
        self.current_day = current_day

        # fond
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((128, 0, 128))

        # boutons
        self.Button_exit = Button(
            Rect(self.width // 2 - 110, self.height - 180, 220, 60),
            'Exit to Desktop', self.screen
        )
        self.Button_home = Button(
            Rect(self.width // 2 - 110, self.height - 110, 220, 60),
            'Return to Home', self.screen
        )

        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

        # scrollbar
        self.scroll_y = 0
        self.scroll_speed = 30
        self.content_height = 1200  # hauteur 

        self.scrollbar_rect = Rect(self.width - 18, 20, 12, self.height - 40)
        self.scroll_thumb_height = 80
        self.scroll_thumb_y = 20
        self.dragging_scroll = False

        self.graph_list = []
        self._build_graphs()

    def _build_graphs(self):
        """
        l'endroit ou on fout les graphes
        """
        figsize_ = [8, 5]
        dpi_ = 100

        #vitesse moyenne
        fig1 = pylab.figure(figsize = figsize_, dpi = dpi_)
        ax1 = fig1.gca()
        ax1.plot([i for i in range(1, self.current_day)], [(sum(speeds) / len(speeds)) for speeds in ([obj.speed for sub in settings.creatures_list_dico[k] for obj in sub] for k in sorted(settings.creatures_list_dico))])
        ax1.set_ylabel('Vitesse moyenne')
        ax1.set_xlabel('Jours')
        self.graph_list.append(self._graph_to_surf(fig1))

        #test
        fig2 = pylab.figure(figsize = figsize_, dpi = dpi_)
        ax2 = fig2.gca()
        ax2.plot([1, 2, 3])
        self.graph_list.append(self._graph_to_surf(fig2))
    

    def _graph_to_surf(self, fig):
        """
        Transforme les graphes en surface affichables sur pygame
        """
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()    
        raw_data = renderer.tostring_argb()
        size = canvas.get_width_height()
        
        surf = pg.image.fromstring(raw_data, size, "RGBA")
        return surf


    def draw(self):
        self.screen.blit(self.bg_asset, (0, 0))

        # surface scrollable
        content_surf = pg.Surface((self.width - 30, self.content_height))
        content_surf.fill((230, 230, 230))

        # affichage des graphes
        y = 30
        for g in self.graph_list:
            content_surf.blit(g, (self.width // 2 - 410, y))
            y += 530

        # affichage dans la fenêtre avec scroll
        self.screen.blit(
            content_surf,
            (0, 0),
            area = Rect(0, self.scroll_y, self.width - 30, self.height)
        )

        # scrollbar
        self._draw_scrollbar()

        # boutons
        self.Button_exit.draw(self.screen, self.Button_font)
        self.Button_home.draw(self.screen, self.Button_font)

    def _draw_scrollbar(self):
        pg.draw.rect(self.screen, (180, 180, 180), self.scrollbar_rect)

        pg.draw.rect(
            self.screen,
            (100, 100, 100),
            Rect(
                self.scrollbar_rect.x,
                self.scroll_thumb_y,
                self.scrollbar_rect.width,
                self.scroll_thumb_height
            )
        )

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.Button_exit.rect.collidepoint(event.pos):
                return 'exit'
            if self.Button_home.rect.collidepoint(event.pos):
                return 'home'
            self.dragging_scroll = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                thumb_rect = Rect(
                    self.scrollbar_rect.x,
                    self.scroll_thumb_y,
                    self.scrollbar_rect.width,
                    self.scroll_thumb_height
                )
                if thumb_rect.collidepoint(event.pos):
                    self.dragging_scroll = True
                    self.drag_offset = event.pos[1] - self.scroll_thumb_y

            if event.button == 4:  # molette haut
                self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
            if event.button == 5:  # molette bas
                self.scroll_y = min(
                    self.content_height - self.height,
                    self.scroll_y + self.scroll_speed
                )
            self._sync_scrollbar()

        if event.type == pg.MOUSEMOTION and self.dragging_scroll:
            self.scroll_thumb_y = event.pos[1] - self.drag_offset
            self.scroll_thumb_y = max(
                self.scrollbar_rect.y,
                min(
                    self.scrollbar_rect.bottom - self.scroll_thumb_height,
                    self.scroll_thumb_y
                )
            )
            self._sync_content_scroll()

    def _sync_scrollbar(self):
        ratio = self.scroll_y / max(1, self.content_height - self.height)
        self.scroll_thumb_y = (
            self.scrollbar_rect.y +
            ratio * (self.scrollbar_rect.height - self.scroll_thumb_height)
        )

    def _sync_content_scroll(self):
        ratio = (
            (self.scroll_thumb_y - self.scrollbar_rect.y) /
            (self.scrollbar_rect.height - self.scroll_thumb_height)
        )
        self.scroll_y = ratio * (self.content_height - self.height)

