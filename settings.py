# Paramètres globaux et valeurs par défaut


creatures_list = [] #liste de liste d'objets ( de creatures ) [[creature 1, ], []]
food_list = []

# Affichage
Display_size = (1280, 720)  # largeur, hauteur
FPS = 30

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

#  Boutons généraux ( et leurs max)
Food_quantity = 20         # Quantité de nourriture initiale
Max_foood_quantity = 1000
Days_max = 1                # Nombre de jours de la simulation 
Max_days_max = 100
day_duration = 5

# limites populations 
POPULATION_MIN = 1
POPULATION_MAX = 6

Color_options = ["white", "red", "green", "blue", "yellow", "purple", "black"]

# Valeurs par défaut pour une population

DEFAULT_POP = {
    "name": "Population 1",
    "life": 50,         #durée de vie mdr je viens de me rendre compte que c'est pas clair mais flemme de changer ( oui c'est un commentaire constructif ET trop long je sais merci )
    "color": "white",
    "quantity": 10,
    "speed_variation": 15,
    "size_variation": 15,
    "view_variation": 15,
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
