#  boucle principale 
import pygame as pg
from Pygame.pygame import Before_Game, Settings, In_Game, Post_Game
import settings
from Game.game import Day_Manager

# --- INIT ---
pg.init()
screen = pg.display.set_mode(settings.Display_size)
clock = pg.time.Clock()

Befg = Before_Game(screen)
Sett = Settings(screen)
Ing = In_Game(screen)
Engd = Post_Game(screen)

day_manager = Day_Manager()

running = True
state = 'home'

# --- MAIN LOOP ---
while running:

    dt = clock.tick(settings.Fps) / 1000.0 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # --- STATE MACHINE ---
        match state:
            case 'home':
                result = Befg.handle_event(event)
                if result == 'start':
                    state = 'settings'
                elif result == 'exit':
                    running = False
                elif result == 'credits':
                    state = 'credits'

            case 'settings':
                result = Sett.handle_event(event)
                if result == 'start':
                    state = 'in_game'

            case 'in_game':
                result = Ing.handle_event(event)
                if result == 'end':
                    state = 'post_game'

            case 'post_game':
                result = Engd.handle_event(event)
                if result == 'exit':
                    running = False
                elif result == 'home':
                    state = 'home'

            case 'credits':
                result = Befg.handle_event(event)
                if result == 'home':
                    state = 'home'

    # --- UPDATE LOGIC ---
    if state == 'in_game':
        if day_manager.update(dt):
            state = 'post_game'

    # --- DRAW ---
    screen.fill((0,0,0))
    match state:
        case 'home':
            Befg.draw()
        case 'settings':
            Sett.draw()
        case 'in_game':
            Ing.draw()
        case 'post_game':
            Engd.draw()
        case 'credits':
            Befg.credits()

    pg.display.flip()




# Fonctionnement theorique du jeu ( en fonctionnement ) dans la boucle main :

# toutes les creatures : listes de liste d'objets ( une liste d'objets par jours, le tout dans une liste globale utilisée pour les stats a la fin)
# la bouffe : liste d'ojets


# debut du jour :
    # - verifier les creatures en vie
    # -les afficher
    # - les mettres a des cos logiques genre pas l'une sur l'autre
    # - faire apparaitre la bouffe
    # -lancer le mouvement des cratures

# faut faire en sorte qu'un jour dure un temps donné
# pendant ce temps faut faire :
    # - a chaques tick faire avancer les creatures ( soit au hasard soit vers de la boufe si jamais y'en as pas loin)
    # -verifier si les cratures ont mangée --> utiliser la methode dans ce cas la

# le tout dans des fonctions avant la boucle principale, on fera des methodes dans une classe game pour certaines choses:
    # - def day(dt --> temps passé depuis la derniere frame, )
    # - def start_day