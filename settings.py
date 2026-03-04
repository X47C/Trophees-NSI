# Paramètres globaux et valeurs par défaut


creatures_list = [] #liste de liste d'objets ( de creatures ) [[creature 1, ..., ... ], [...], ...]
food_list = []
creatures_list_dico = {} #a la fin de chaques jours on va mettre le liste de liste de creature acutelle dans le dictionnaire avec comme cle le numero du jour pour faire les graphes de fin le commentaire est trop long ptndrrr
food_list_dico = {}
editable_butons = {}


# Affichage
Display_size = (1280, 720)  # largeur, hauteur
FPS = 60

# texte des crédits
Credits_Text = ['Dévellopé par : ','Cyprien Cros', 'Jules Graffan', 'Sarah Vignaud-Quantin', 'Remerciement à : ', 'Mme Rebinguet-Martres'] 

# Police 
Days_font = "arial"
Days_font_size = 18
Button_font = "arial" 
Button_font_size = 18
Button_label_font = "arial"
Button_label_font_size = 14
Credits_font = 'arial'
Credits_font_size = 18

#  Boutons généraux (et leurs max)
Max_foood_quantity = 100
Days_max = 5               # Nombre de jours de la simulation 
Max_days_max = 100
Food_quantity_default = 40
Food_quantity = [Food_quantity_default] * Days_max  # liste : quantité par jour

def food_for_day(day_index:int) -> int:
    """Retourne la quantité pour un jour (1-based)."""
    i = max(0, min(len(Food_quantity)-1, day_index-1))
    return Food_quantity[i]
def sync_food_quantity():
    """Assure que la liste Food_quantity a exactement Days_max éléments."""
    global Food_quantity
    if len(Food_quantity) < Days_max:
        Food_quantity.extend([Food_quantity_default] * (Days_max - len(Food_quantity)))
    elif len(Food_quantity) > Days_max:
        Food_quantity = Food_quantity[:Days_max]



# limites populations 
POPULATION_MIN = 1
POPULATION_MAX = 6

Color_options = ["blue", "pink", "red", "green", "yellow", "purple", "gray"]

# Valeurs par défaut pour une population

DEFAULT_POP = {
    "name": "Population 1",
    "life": 50,         #durée de vie mdr je viens de me rendre compte que c'est pas clair mais flemme de changer ( oui c'est un commentaire constructif ET trop long je sais merci )
    "color": "blue",
    "quantity": 10,
    "speed_variation": 30,
    "size_variation": 30,
    "view_variation": 30,
    "view": 4,
    "speed": 4,
    "size": 4
}

# Valeurs par défaut pour une population : MAX
Max_life = 53
Max_quantity = 100
Max_caracteristic = 10 # size, view et speed ( mais je sais meme pas si c'est un mot anglais mais chilll ) 

# Liste des populations ( au moins 1 )
POPULATIONS = [
    DEFAULT_POP.copy()
]

# UI colors
UI_BG_COLOR = (200, 200, 200)
UI_PANEL_COLOR = (240, 240, 240)

# Toolbox
toolbox_show_day = True
toolbox_show_creatures = True
toolbox_show_food = True
toolbox_show_vision = True
toolbox_simulation_speed = 1  # multiplicateur : 0.5, 1, 2, 4, 8, 16
