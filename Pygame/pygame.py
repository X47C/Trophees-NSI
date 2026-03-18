# ensemble des classes gérant les différents écrans du jeu
import pygame as pg
from Pygame.button import Button
from Pygame.toolbox import Toolbox
from pygame import Rect
import settings
import matplotlib as plt
plt.use("Agg")  # backend sans fenêtre
import pylab
import matplotlib.backends.backend_agg as agg
from matplotlib.ticker import MaxNLocator
import cv2


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

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 - 40, 220, 80),'', self.screen)
        self.Button_Start = Button(Rect(self.width // 2 - 110, self.height // 2 - 130, 220, 80),'', self.screen)
        self.Button_credits = Button(Rect(self.width // 2 - 110, self.height // 2 + 50, 220, 80),'', self.screen) 
        self.Button_credits_exit = Button(Rect(self.width // 2 - 65, self.height // 2 + 130, 130, 50),'Back', self.screen)
        self.Button_tutorial = Button(Rect(self.width // 2 - 110, self.height // 2 + 140, 220, 80),'Tutoriale', self.screen) 
        self.Button_tutorial_pass = Button(Rect(self.width // 2 - 65, self.height // 2 + 50, 130, 50),'Pass', self.screen)

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
        self.Button_tutorial.draw(self.screen, self.Button_font) 


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
                if self.Button_tutorial.rect.collidepoint(event.pos):
                    return 'tutorial'



    def tutorial(self):
        """
        Affiche le tutoriel sous forme de popup par-dessus l'écran d'accueil.
        Utilise opencv pour lire la vidéo frame par frame et l'afficher dans pygame.
        """

        # chargement de la vidéo
        cap = cv2.VideoCapture('assets/video_test.mp4')

        fps_video = cap.get(cv2.CAP_PROP_FPS) or 30
        clock_tuto = pg.time.Clock()

        # dimensions de la popup
        popup_w = int(self.width * 0.75)
        popup_h = int(self.height * 0.75)
        popup_x = (self.width - popup_w) // 2
        popup_y = (self.height - popup_h) // 2

        # hauteur réservée pour le bouton "Passer" en bas de la popup
        btn_zone_h = 60
        video_h = popup_h - btn_zone_h

        # bouton "Passer" centré en bas de la popup
        btn_w, btn_h = 130, 44
        btn_x = popup_x + (popup_w - btn_w) // 2
        btn_y = popup_y + popup_h - btn_zone_h + (btn_zone_h - btn_h) // 2
        self.Button_tutorial_pass.rect = pg.Rect(btn_x, btn_y, btn_w, btn_h)

        running_tuto = True
        while running_tuto:
            self.draw()

            # lecture d'une frame
            ret, frame = cap.read()
            if not ret:
                # fin de la vidéo : on arrete
                running_tuto = False
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (popup_w, video_h))
            frame_surf = pg.surfarray.make_surface(frame_rgb.swapaxes(0, 1))

            # fond semi-transparent par-dessus l'écran d'accueil
            overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            # fond de la popup
            pg.draw.rect(self.screen, (255, 255, 255), (popup_x - 15, popup_y - 15, popup_w + 30, popup_h + 15), border_radius=8)

            # affichage de la frame vidéo
            self.screen.blit(frame_surf, (popup_x, popup_y))

            # bouton "Passer"
            self.Button_tutorial_pass.draw(self.screen, self.Button_font)

            pg.display.flip()
            clock_tuto.tick(fps_video)

            # gestion des événements
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running_tuto = False
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if self.Button_tutorial_pass.rect.collidepoint(event.pos):
                        running_tuto = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running_tuto = False

        cap.release()


    def credits(self):
        """
        Affiche les crédits du jeu
        A modifier avec une image quand on en aura une
        """
        pg.draw.rect(self.screen, (255, 255, 255), (100, 100, self.width - 200, self.height - 200))
        self.Button_credits_exit.draw(self.screen, self.Button_font)
        for i in range(len(settings.Credits_Text)):
            self.screen.blit(pg.font.SysFont(settings.Credits_font, settings.Credits_font_size).render(settings.Credits_Text[i], True, (0, 0, 0)), (self.width // 2 - 150, 130 + 80 * i))




class Settings:
    """
    permet de gérer l'écran des paramètres de la simulation
    """

    def __init__(self, screen: pg.surface):
        self.screen = screen
        self.width, self.height = settings.Display_size

        #polices
        self.font_btn = pg.font.SysFont(settings.Button_font, settings.Button_font_size)
        self.font_lbl = pg.font.SysFont(settings.Button_label_font, settings.Button_label_font_size)

        #dimensions des éléments
        settings.PostG_PADDING = 20
        self.gap = 30
        self.btn_h = 44
        self.small_w = 48
        self.label_gap = 12

        # couleur de fond pour le bouton numéroté sélectionné
        self.pop_selected_bg = (120, 200, 140)

        #espaces autour de la zone de gestion des populations
        self.pop_manage_top_space = 60
        self.pop_manage_bottom_space = 48

        #index de la population sélectionnée
        self.selected_pop = 0

        #construction de l'interface
        self.build_general_controls()
        self.build_pop_management_buttons()
        self.build_pop_controls()
        self.build_bottom_buttons()


    def update_layout(self):
        """
        Reconstruit toute l'interface en conservant la population sélectionnée.
        """
        sel = self.selected_pop
        self.build_general_controls()
        self.build_pop_management_buttons()
        self.build_pop_controls()
        self.build_bottom_buttons()
        self.selected_pop = sel
        self.editable_button_set_value()
        self.refresh_pop_display()


    def build_general_controls(self):
        """
        Construit les contrôles généraux : nourriture et nombre de jours.
        """
        total_w = self.width - settings.PostG_PADDING * 2
        col_w = (total_w - self.gap) // 2
        val_w = col_w - self.small_w * 2 - 12
        top_y = settings.PostG_PADDING

        # bouton nourriture à gauche
        x0 = settings.PostG_PADDING
        lbl_y = top_y
        btn_y = lbl_y + self.font_lbl.get_height() + self.label_gap
        col_w = (total_w - self.gap) // 2

        settings.editable_butons['food_qtt'] = Button(Rect(x0, btn_y, col_w, self.btn_h), "Modifier", self.screen, description="Permet d'acceder à une fenetre permettant de gérer la quantité de nouriture de la simulation au cours du temps")
        self.general_food = {"label": "Quantité de nourriture", "value": settings.editable_butons['food_qtt'], "lbl_pos": (x0 + (col_w // 2), lbl_y)}

        # bouton jours à droite
        x1 = settings.PostG_PADDING + col_w + self.gap
        lbl_y = top_y
        btn_y = lbl_y + self.font_lbl.get_height() + self.label_gap
        settings.editable_butons['day_qtt'] = Button(Rect(x1 + self.small_w + 6, btn_y, val_w, self.btn_h), str(settings.Days_max), self.screen, editable=True, max_length=100, description="Permet de modifier le nombre de jours de la simulation, avec au minimum 1 jour et au maximum 100 jours.")
        self.general_days = {"label": "Nombre de jours de la simulation", "minus": Button(Rect(x1, btn_y, self.small_w, self.btn_h), "-", self.screen), "value": settings.editable_butons['day_qtt'], "plus": Button(Rect(x1 + self.small_w + 6 + val_w + 6, btn_y, self.small_w, self.btn_h), "+", self.screen), "lbl_pos": (x1 + (col_w // 2), lbl_y)}

        base_line = btn_y + self.btn_h
        self.pop_manage_y = base_line + self.pop_manage_top_space
        self.pop_controls_start_y = self.pop_manage_y + 36 + self.pop_manage_bottom_space


    def build_pop_management_buttons(self):
        """
        Construit les boutons d'ajout, suppression et sélection de population.
        """
        y = self.pop_manage_y

        self.btn_add_pop = Button(Rect(settings.PostG_PADDING, y, 110, 36), "+ Pop", self.screen, description="Permet de d'augmenter le nombre de populations de la simulation, avec un maximum de 6")
        self.btn_rem_pop = Button(Rect(settings.PostG_PADDING + 120, y, 110, 36), "- Pop", self.screen, description="Permet diminuer le nombre de populations de la simulation, avec un minimum de 1")

        # petits boutons numérotés pour chaque population
        self.pop_number_buttons = []
        x = settings.PostG_PADDING + 260
        for i in range(len(settings.POPULATIONS)):
            rect = Rect(x, y, 40, 36)
            self.pop_number_buttons.append((rect, i))
            x += 46


    def build_pop_controls(self):
        """
        Construit la grille de contrôles pour la population sélectionnée.
        """
        # crée une population par défaut si la liste est vide
        if len(settings.POPULATIONS) == 0:
            if hasattr(settings, 'DEFAULT_POP'):
                settings.POPULATIONS.append(settings.DEFAULT_POP.copy())
            else:
                settings.POPULATIONS.append({"name": "Population 1", "life": 50, "color": "blue", "quantity": 10, "speed_variation": 15, "size_variation": 15, "view_variation": 15, "view": 15, "speed": 3, "size": 3})

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

        # descriptions pour chaque champ
        descriptions = {
            "life": "Permet de définir au bout de combien de jours une créature meurt de vieillesse, même si elle a mangé",
            "color": "Défini la couleur de chaque population",
            "quantity": "Permet de definir le nombre de créatures de cette population au début de la simulation",
            "speed_variation": "Permet de definir le taux de transmission de la vitesse aux enfants des créatures",
            "size_variation": "Permet de definir le taux de transmission de la taille aux enfants des créatures",
            "view_variation": "Permet de definir le taux de transmission du champ de vision aux enfants de ces créatures",
            "view": "Permet de definir le champ de vision des créatures de cette population au début de la simulation",
            "speed": "Permet de definir la vitesse des créatures de cette population au début de la simulation",
            "size": "Permet de definir la taille des créatures de cette population au début de la simulation",
        }

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
            if key == "life": 
                description = "Permet de définir au bout de combien de jours une créature meurt de vieillesse, même si elle a mangé"
            if key == "color":
                description = "Permet de choisir la couleur de chaque population, les couleurs défilent lorsque l'on appuie sur + ou -"
            if key == "quantity":
                description = "Permet de définir le nombre de créatures au début de la simulation"
            if key == "speed_variation":
                description = "Permet de définir à quel point la vitesse des créatures varie au fur et à mesure de leur évolution, chaque jour de la simulation"
            if key == "size_variation":
                description = "Permet de définir à quel point la taille des créatures varie au fur et à mesure de leur évolution, chaque jour de la simulation"
            if key == "view_variation":
                description = "Permet de définir à quel point le champ de vision des créatures varie au fur et à mesure de leur évolution, chaque jour de la simulation"
            if key == "view":
                description = "Permet de définir le champ de vision des créatures au début de la simulation"
            if key == "speed":
                description = "Permet de définir la vitesse des créatures au début de la simulation"
            if key == "size":
                description = "Permet de définir la taille des créatures au début de la simulation"

            description = descriptions.get(key, "")
            minus = Button(Rect(x, y_btn, self.small_w, self.btn_h), "-", self.screen)
            if isinstance(cur_val, int):
                value = Button(Rect(x + self.small_w + 6, y_btn, val_w, self.btn_h), display, self.screen, editable=True, description=description)
            else:
                value = Button(Rect(x + self.small_w + 6, y_btn, val_w, self.btn_h), display, self.screen, description=description)
            plus = Button(Rect(x + self.small_w + 6 + val_w + 6, y_btn, self.small_w, self.btn_h), "+", self.screen)

            center_x = x + (col_w // 2)
            self.pop_controls[key] = {"label": label, "label_pos": (center_x, y_label), "minus": minus, "value": value, "plus": plus}


    def build_bottom_buttons(self):
        """
        Construit les boutons Start et Back en bas de l'écran.
        """
        y = self.height - (self.btn_h + 20)
        w = 220
        gap = 24
        x = (self.width - (2 * w + gap)) // 2
        self.btn_start = Button(Rect(x, y, w, self.btn_h), "Start", self.screen)
        self.btn_back = Button(Rect(x + w + gap, y, w, self.btn_h), "Back", self.screen)


    def draw(self):
        """
        Dessine l'écran des paramètres avec tous ses contrôles.
        """
        self.screen.fill(settings.UI_BG_COLOR if hasattr(settings, 'UI_BG_COLOR') else (200, 200, 200))
        pg.draw.rect(self.screen, settings.UI_PANEL_COLOR if hasattr(settings, 'UI_PANEL_COLOR') else (240, 240, 240), (0, 0, self.width, self.height))

        # nourriture
        g = self.general_food
        label_surf = self.font_lbl.render(g["label"], True, (0, 0, 0))
        cx, ly = g["lbl_pos"]
        lx = int(cx - label_surf.get_width() // 2)
        self.screen.blit(label_surf, (lx, ly))
        g["value"].draw(self.screen, self.font_btn)

        # durée de la simulation
        g = self.general_days
        label_surf = self.font_lbl.render(g["label"], True, (0, 0, 0))
        cx, ly = g["lbl_pos"]
        lx = int(cx - label_surf.get_width() // 2)
        self.screen.blit(label_surf, (lx, ly))
        g["minus"].draw(self.screen, self.font_btn)
        g["value"].draw(self.screen, self.font_btn)
        g["plus"].draw(self.screen, self.font_btn)

        # boutons de gestion des populations
        self.btn_add_pop.draw(self.screen, self.font_btn)
        self.btn_rem_pop.draw(self.screen, self.font_btn)

        # boutons numérotés des populations
        for rect, i in self.pop_number_buttons:
            if i == self.selected_pop:
                pg.draw.rect(self.screen, self.pop_selected_bg, (rect.x, rect.y, rect.width, rect.height))
                txt = self.font_btn.render(str(i + 1), True, (255, 255, 255))
                tx = rect.x + (rect.width - txt.get_width()) // 2
                ty = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx, ty))
            else:
                b = Button(Rect(rect.x, rect.y, rect.width, rect.height), str(i + 1), self.screen)
                b.draw(self.screen, self.font_btn)

        # grille des contrôles de la population sélectionnée
        for key, c in self.pop_controls.items():
            label_surf = self.font_lbl.render(c["label"], True, (0, 0, 0))
            cx, ly = c["label_pos"]
            lx = int(cx - label_surf.get_width() // 2)
            self.screen.blit(label_surf, (lx, ly))
            c["minus"].draw(self.screen, self.font_btn)
            c["value"].draw(self.screen, self.font_btn)
            c["plus"].draw(self.screen, self.font_btn)

        # boutons du bas
        self.btn_start.draw(self.screen, self.font_btn)
        self.btn_back.draw(self.screen, self.font_btn)

        # descriptions au dessus de tout le reste
        settings.editable_butons['food_qtt'].description()
        settings.editable_butons['day_qtt'].description()
        self.btn_add_pop.description()
        self.btn_rem_pop.description()
        for key, c in self.pop_controls.items():
            c['value'].description()
        self.btn_start.description()
        self.btn_back.description()


    def handle_event(self, event):
        """
        Gère les clics sur tous les boutons de l'écran des paramètres.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.general_food["value"].rect.collidepoint(event.pos):
                return 'edit_food_curve'
            if self.btn_start.rect.collidepoint(event.pos):
                return 'start'
            if self.btn_back.rect.collidepoint(event.pos):
                return 'back'

            mx, my = event.pos

            # contrôles généraux
            if self.general_days["minus"].rect.collidepoint((mx, my)):
                settings.Days_max = max(1, settings.Days_max - 1)
                settings.sync_food_quantity()
                self.editable_button_set_value()
                return None
            if self.general_days["plus"].rect.collidepoint((mx, my)):
                settings.Days_max = min(settings.Max_days_max, settings.Days_max + 1)
                settings.sync_food_quantity()
                self.editable_button_set_value()
                return None

            # ajout ou suppression d'une population
            if self.btn_add_pop.rect.collidepoint((mx, my)):
                if len(settings.POPULATIONS) < settings.POPULATION_MAX:
                    new_idx = len(settings.POPULATIONS) + 1
                    base = settings.DEFAULT_POP.copy() if hasattr(settings, 'DEFAULT_POP') else {"name": f"Population {new_idx}", "life": 50, "color": "blue", "quantity": 10, "speed_variation": 15, "size_variation": 15, "view_variation": 15, "view": 15, "speed": 3, "size": 3}
                    base["name"] = f"Population {new_idx}"
                    available = settings.get_available_colors()
                    base['color'] = available[0] if available else settings.Color_options[0]
                    settings.POPULATIONS.append(base)
                    self.selected_pop = len(settings.POPULATIONS) - 1
                    self.build_pop_management_buttons()
                    self.build_pop_controls()
                    self.editable_button_set_value()
                return None

            if self.btn_rem_pop.rect.collidepoint((mx, my)):
                if len(settings.POPULATIONS) > settings.POPULATION_MIN:
                    settings.POPULATIONS.pop(self.selected_pop)
                    self.selected_pop = max(0, min(self.selected_pop, len(settings.POPULATIONS) - 1))
                    self.build_pop_management_buttons()
                    self.build_pop_controls()
                    self.editable_button_set_value()
                return None

            # sélection d'une population par son numéro
            for rect, idx in self.pop_number_buttons:
                if rect.collidepoint((mx, my)):
                    self.selected_pop = idx
                    self.build_pop_controls()
                    self.editable_button_set_value()
                    return None

            if len(settings.POPULATIONS) == 0:
                return None

            # boutons - et + des caractéristiques de la population
            pop = settings.POPULATIONS[self.selected_pop]
            for key, c in self.pop_controls.items():
                if c["minus"].rect.collidepoint((mx, my)):
                    cur = pop.get(key)
                    if key == "color":
                        opts_all = getattr(settings, 'Color_options', [])
                        opts = settings.get_available_colors(exclude_pop_index=self.selected_pop)
                        cur_color = pop.get("color")
                        cycle = [c for c in opts_all if c in opts or c == cur_color]
                        if cycle:
                            try:
                                i = cycle.index(cur_color)
                            except ValueError:
                                i = 0
                            pop["color"] = cycle[(i - 1) % len(cycle)]
                    elif isinstance(cur, int):
                        pop[key] = max(0, cur - 1)
                    self.editable_button_set_value()
                    return None

                if c["plus"].rect.collidepoint((mx, my)):
                    cur = pop.get(key)
                    match key:
                        case 'color':
                            opts_all = getattr(settings, 'Color_options', [])
                            opts = settings.get_available_colors(exclude_pop_index=self.selected_pop)
                            cur_color = pop.get("color")
                            cycle = [c for c in opts_all if c in opts or c == cur_color]
                            if cycle:
                                try:
                                    i = cycle.index(cur_color)
                                except ValueError:
                                    i = 0
                                pop["color"] = cycle[(i + 1) % len(cycle)]
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
                            pop[key] = min(cur + 1, 100) # pourcentage, max 100
                        case 'view_variation':
                            pop[key] = min(cur + 1, 100) # pourcentage, max 100
                        case 'speed_variation':
                            pop[key] = min(cur + 1, 100) # pourcentage, max 100
                    self.editable_button_set_value()
                    return None

        self.editable_button_save_value()
        return None


    def editable_button_refresh(self, event):
        """
        Propage les événements clavier aux boutons éditables.
        """
        for b in settings.editable_butons.values():
            b.handle_event(event)
        for b in self.pop_controls.values():
            b['value'].handle_event(event)


    def editable_button_set_value(self):
        """
        Met à jour l'affichage de tous les boutons éditables depuis les settings.
        """
        settings.editable_butons['day_qtt'].set_value(settings.Days_max)

        pop = settings.POPULATIONS[self.selected_pop]
        for key, c in self.pop_controls.items():
            if key != "color":
                c['value'].set_value(pop[key])
            else:
                c["value"].text = str(pop.get(key, ""))


    def editable_button_save_value(self):
        """
        Sauvegarde les valeurs saisies dans les boutons éditables vers les settings.
        """
        # sauvegarde du nombre de jours
        if isinstance(settings.editable_butons['day_qtt'].get_number(), int):
            settings.Days_max = min(settings.Max_days_max, settings.editable_butons['day_qtt'].get_number())
            settings.sync_food_quantity()
            settings.editable_butons['day_qtt'].set_value(settings.Days_max)
        else:
            settings.Days_max = int(settings.editable_butons['day_qtt'].text)
            settings.sync_food_quantity()

        # sauvegarde des caractéristiques de la population
        pop = settings.POPULATIONS[self.selected_pop]
        for key, c in self.pop_controls.items():
            if key != "color":
                if isinstance(c['value'].get_number(), int):
                    match key:
                        case 'life':
                            pop[key] = min(c['value'].get_number(), settings.Max_life)
                            c['value'].set_value(pop[key])
                        case 'quantity':
                            pop[key] = min(c['value'].get_number(), settings.Max_quantity)
                            c['value'].set_value(pop[key])
                        case 'size':
                            pop[key] = min(c['value'].get_number(), settings.Max_caracteristic)
                            c['value'].set_value(pop[key])
                        case 'speed':
                            pop[key] = min(c['value'].get_number(), settings.Max_caracteristic)
                            c['value'].set_value(pop[key])
                        case 'view':
                            pop[key] = min(c['value'].get_number(), settings.Max_caracteristic)
                            c['value'].set_value(pop[key])
                        case 'size_variation':
                            pop[key] = min(c['value'].get_number(), 100)
                            c['value'].set_value(pop[key])
                        case 'view_variation':
                            pop[key] = min(c['value'].get_number(), 100)
                            c['value'].set_value(pop[key])
                        case 'speed_variation':
                            pop[key] = min(c['value'].get_number(), 100)
                            c['value'].set_value(pop[key])
                else:
                    pop[key] = int(c['value'].text)
            else:
                c["value"].text = str(pop.get(key, ""))




class In_Game:
    """
    permet de gérer l'écran pendant la partie
    """
    def __init__(self, screen: pg.surface):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran pendant la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen

        # self.bg_asset = pg.image.load('assets/bg_in_game.png')
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((34, 139, 34))

        self.toolbox = Toolbox(screen)


    def draw(self, l_creatures: list, screen: pg.surface) -> None:
        """
        Dessine l'écran pendant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))

        # affiche les créatures et la nourriture
        for a in l_creatures:
            for c in a:
                c.draw(screen)
        for f in settings.food_list:
            f.draw(screen)
        self.toolbox.draw()


    def handle_event(self, event: pg.event) -> str:
        """
        Gère les événements de l'écran pendant la partie
        """
        result = self.toolbox.handle_event(event)
        if result == 'end':
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

        #fond blanc
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((255, 255, 255))

        #boutons de navigation
        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height - 180, 220, 60), 'Exit to Desktop', self.screen)
        self.Button_home = Button(Rect(self.width // 2 - 110, self.height - 110, 220, 60), 'Return to Home', self.screen)
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

        #scrollbar
        self.scroll_y = 0
        self.scroll_speed = 30
        self.scrollbar_rect = Rect(self.width - 18, 20, 12, self.height - 40)
        self.scroll_thumb_height = 80
        self.scroll_thumb_y = 20
        self.dragging_scroll = False

        #construction des graphes
        self.graph_list = []
        g_nb = self.build_graphs()
        self.content_height = 540 * g_nb


    def build_graphs(self):
        """
        l'endroit ou on fout les graphes
        """
        #paramètres communs
        lw = 1 # épaisseur des courbes
        jour = [i for i in range(1, self.current_day + 1)]
        figsize = [8, 5]
        dpi = 100
        g_nb = 0

        days = sorted(settings.creatures_list_dico)

        # graphe 1 : caractéristiques moyennes toutes populations
        fig1 = pylab.figure(figsize=figsize, dpi=dpi)
        ax1 = fig1.gca()

        avrage_speed = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.speed for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]
        average_size = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.size for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]
        average_view = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.view for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]


        ax1.set_xlim(0.5, self.current_day + 0.5)
        ax1.xaxis.set_major_locator(MaxNLocator(nbins=12, integer=True))
        ax1.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax1.set_ylim(0, 10)
        ax1.set_yticks(range(0, 11))
        ax1.plot(jour, avrage_speed, label="Vitesse", lw=lw, marker='+')
        ax1.plot(jour, average_size, label="Taille", lw=lw, marker="x")
        ax1.plot(jour, average_view, label="Vue", lw=lw, marker="o")
        ax1.set_xlabel('Jours')
        ax1.set_ylabel('Moyenne')
        ax1.set_title("Évolution des caractéristiques moyennes (toutes populations)", fontsize=13, fontweight='bold', pad=12)
        ax1.legend(loc='upper left', framealpha=0.8)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.set_axisbelow(True)
        fig1.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig1))
        pylab.close(fig1)
        g_nb += 1

        # graphe 2 : nombre de créatures et de nourriture
        fig2 = pylab.figure(figsize=figsize, dpi=dpi)
        ax2 = fig2.gca()

        c_counts = [sum(len(sub) for sub in settings.creatures_list_dico[k]) for k in range(1, len(settings.creatures_list_dico) + 1)]
        f_counts = [settings.food_list_dico[i] for i in range(1, len(settings.food_list_dico) + 1)]

        ax2.set_xlim(0.5, self.current_day + 0.5)
        ax2.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
        ax2.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax2.plot(jour, c_counts, label='Créature', lw=lw, marker="x")
        ax2.plot(jour, f_counts, label='Nouriture', lw=lw, marker="o")
        ax2.set_xlabel('Jours')
        ax2.set_ylabel('Quantitée')
        ax2.set_title("Évolution de la quantité de créatures et de la quantité de nouriture", fontsize=13, fontweight='bold', pad=12)
        ax2.legend(loc='upper left', framealpha=0.8)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.set_axisbelow(True)
        fig2.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig2))
        pylab.close(fig2)
        g_nb += 1

        # graphe 3 : quantité par population
        fig3 = pylab.figure(figsize=figsize, dpi=dpi)
        ax3 = fig3.gca()

        for i in range(len(settings.creatures_list_dico[1])):
            c_p_conts = [len(p[i]) for p in settings.creatures_list_dico.values()]
            ax3.plot(jour, c_p_conts, lw=lw, color=settings.creatures_list_dico[1][i][0].color)
        ax3.set_xlim(0.5, self.current_day + 0.5)
        ax3.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
        ax3.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax3.set_xlabel('Jours')
        ax3.set_ylabel('Quantité')
        ax3.set_title("Évolution de la quantité de créatures par populations", fontsize=13, fontweight='bold', pad=12)
        ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax3.grid(True, linestyle='--', alpha=0.5)
        ax3.set_axisbelow(True)
        fig3.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig3))
        pylab.close(fig3)
        g_nb += 1

        # graphes 4+ : caractéristiques par population
        for i in range(len(settings.creatures_list)):
            color = settings.creatures_list_dico[1][i][0].color

            fig4 = pylab.figure(figsize=figsize, dpi=dpi)
            ax4 = fig4.gca()

            ax4.set_xlim(0.5, self.current_day + 0.5)
            ax4.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
            ax4.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
            ax4.set_ylim(0, 10)
            ax4.set_yticks(range(0, 11))

            m_speed = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.speed for c in settings.creatures_list_dico[d][i]] for d in days)]
            m_size = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.size for c in settings.creatures_list_dico[d][i]] for d in days)]
            m_view = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.view for c in settings.creatures_list_dico[d][i]] for d in days)]

            ax4.plot(jour, m_speed, label="Vitesse", lw=lw, marker='+', color=color)
            ax4.plot(jour, m_size, label="Taille", lw=lw, marker="x", color=color)
            ax4.plot(jour, m_view, label="Vue", lw=lw, marker="o", color=color)
            ax4.set_xlabel('Jours')
            ax4.set_ylabel('Moyenne')
            ax4.set_title(f"Évolution des caractéristiques moyennes de la population {color}", fontsize=13, fontweight='bold', pad=12)
            ax4.legend(loc='upper left', framealpha=0.8)
            ax4.grid(True, linestyle='--', alpha=0.5)
            ax4.set_axisbelow(True)
            fig4.tight_layout()
            self.graph_list.append(self.graph_to_surf(fig4))
            pylab.close(fig4)
            g_nb += 1

        return g_nb


    def graph_to_surf(self, fig):
        """
        Transforme les graphes en surface affichables sur pygame
        """
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_argb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "ARGB")
        surf = surf.convert_alpha()
        return surf


    def draw(self):
        """
        Dessine l'écran post-partie avec les graphes et la scrollbar.
        """
        self.screen.blit(self.bg_asset, (0, 0))

        # surface scrollable contenant les graphes
        content_surf = pg.Surface((self.width - 30, self.content_height))
        content_surf.fill((230, 230, 230))

        y = 30
        for g in self.graph_list:
            content_surf.blit(g, (self.width // 2 - 410, y))
            y += 530

        self.screen.blit(content_surf, (0, 0), area=Rect(0, self.scroll_y, self.width - 30, self.height))

        self.draw_scrollbar()
        self.Button_exit.draw(self.screen, self.Button_font)
        self.Button_home.draw(self.screen, self.Button_font)


    def draw_scrollbar(self):
        """
        Dessine la scrollbar et son curseur.
        """
        pg.draw.rect(self.screen, (180, 180, 180), self.scrollbar_rect)
        pg.draw.rect(self.screen, (100, 100, 100), Rect(self.scrollbar_rect.x, self.scroll_thumb_y, self.scrollbar_rect.width, self.scroll_thumb_height))


    def handle_event(self, event):
        """
        Gère le scroll et les clics sur les boutons de navigation.
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.Button_exit.rect.collidepoint(event.pos):
                return 'exit'
            if self.Button_home.rect.collidepoint(event.pos):
                return 'home'
            self.dragging_scroll = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                thumb_rect = Rect(self.scrollbar_rect.x, self.scroll_thumb_y, self.scrollbar_rect.width, self.scroll_thumb_height)
                if thumb_rect.collidepoint(event.pos):
                    self.dragging_scroll = True
                    self.drag_offset = event.pos[1] - self.scroll_thumb_y
            if event.button == 4: # molette haut
                self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
            if event.button == 5: # molette bas
                self.scroll_y = min(self.content_height - self.height, self.scroll_y + self.scroll_speed)
            self.sync_scrollbar()

        if event.type == pg.MOUSEMOTION and self.dragging_scroll:
            self.scroll_thumb_y = event.pos[1] - self.drag_offset
            self.scroll_thumb_y = max(self.scrollbar_rect.y, min(self.scrollbar_rect.bottom - self.scroll_thumb_height, self.scroll_thumb_y))
            self.sync_content_scroll()


    def sync_scrollbar(self):
        """
        Met à jour la position du curseur de la scrollbar depuis le scroll actuel.
        """
        ratio = self.scroll_y / max(1, self.content_height - self.height)
        self.scroll_thumb_y = self.scrollbar_rect.y + ratio * (self.scrollbar_rect.height - self.scroll_thumb_height)


    def sync_content_scroll(self):
        """
        Met à jour le scroll depuis la position du curseur de la scrollbar.
        """
        ratio = (self.scroll_thumb_y - self.scrollbar_rect.y) / (self.scrollbar_rect.height - self.scroll_thumb_height)
        self.scroll_y = ratio * (self.content_height - self.height)