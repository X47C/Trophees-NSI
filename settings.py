# paramètres globaux et valeurs par défaut


creatures_list = [] # liste de liste de créatures : [[creature, ...], [...], ...]
food_list = []
creatures_list_dico = {} # à la fin de chaque jour on stocke la liste de créatures avec le numéro du jour comme clé, pour les graphes de fin
food_list_dico = {}
editable_butons = {}


# affichage
Display_size = (1280, 720)  # largeur, hauteur
FPS = 60
PostG_PADDING = 20


# polices
Days_font = "arial"
Days_font_size = 18
Button_font = "arial"
Button_font_size = 18
Button_label_font = "arial"
Button_label_font_size = 14
Credits_font = 'arial'
Credits_font_size = 18

# boutons généraux et leurs limites
Max_foood_quantity = 100
Days_max = 5               # nombre de jours de la simulation
Max_days_max = 500
Food_quantity_default = 40
Food_quantity = [Food_quantity_default] * Days_max  # liste : quantité par jour


def food_for_day(day_index: int) -> int:
    """Retourne la quantité pour un jour (1-based)."""
    i = max(0, min(len(Food_quantity) - 1, day_index - 1))
    return Food_quantity[i]


def sync_food_quantity():
    """Assure que la liste Food_quantity a exactement Days_max éléments."""
    global Food_quantity
    if len(Food_quantity) < Days_max:
        Food_quantity.extend([Food_quantity_default] * (Days_max - len(Food_quantity)))
    elif len(Food_quantity) > Days_max:
        Food_quantity = Food_quantity[:Days_max]


# limites des populations
POPULATION_MIN = 1
POPULATION_MAX = 6

Color_options = ["blue", "pink", "red", "green", "yellow", "purple", "gray"]


def get_used_colors(exclude_pop_index=None):
    """Retourne l'ensemble des couleurs déjà utilisées par les populations,
    en excluant optionnellement une population (par son index)."""
    used = set()
    for i, pop in enumerate(POPULATIONS):
        if i != exclude_pop_index:
            used.add(pop["color"])
    return used


def is_color_available(color, exclude_pop_index=None):
    """Renvoie True si la couleur n'est pas déjà utilisée par une autre population."""
    return color not in get_used_colors(exclude_pop_index)


def get_available_colors(exclude_pop_index=None):
    """Renvoie la liste des couleurs encore disponibles."""
    used = get_used_colors(exclude_pop_index)
    return [c for c in Color_options if c not in used]


# valeurs par défaut pour une population
DEFAULT_POP = {
    "name": "Population 1",
    "life": 50,         # durée de vie de la créature sur une journée
    "color": "blue",
    "quantity": 10,
    "speed_variation": 30,
    "size_variation": 30,
    "view_variation": 30,
    "view": 4,
    "speed": 4,
    "size": 4
}

# valeurs maximales des caractéristiques
Max_life = 53
Max_quantity = 100
Max_caracteristic = 10  # s'applique à size, view et speed

# liste des populations (au moins 1)
POPULATIONS = [DEFAULT_POP.copy()]

# couleurs de l'interface
UI_BG_COLOR = (200, 200, 200)
UI_PANEL_COLOR = (240, 240, 240)

# toolbox
toolbox_show_day = True
toolbox_show_creatures = True
toolbox_show_food = True
toolbox_show_vision = True
toolbox_simulation_speed = 1  # multiplicateur : 0.5, 1, 2, 4, 8, 16

# noms des couleurs des populations 
#les noms au masculin pour les boutons :
dico1 = {"blue" : "bleu", "pink" : "rose", "red" : "rouge", "green" : "vert", "yellow" : "jaune", "purple" : "violet", "gray" : "gris"}
#les noms au feminin pour les graphiques :
dico2 = {"blue" : "bleue", "pink" : "rose", "red" : "rouge", "green" : "verte", "yellow" : "jaune", "purple" : "violette", "gray" : "grise"}