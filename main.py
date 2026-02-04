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

day_manager = Day_Manager(screen)

running = True
state = 'home'


# --- MAIN LOOP ---
while running:

    # --- EVENT HANDLING ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        match state:
            case 'home':
                match Befg.handle_event(event):
                    case 'start':
                        state = 'settings'
                    case 'exit':
                        running = False
                    case 'credits':
                        state = 'credits'

            case 'settings':
                match Sett.handle_event(event):
                    case'start':
                        day_manager.first_day()
                        state = 'in_game'
                    case 'back':
                        state = 'home'

            case 'in_game':
                match Ing.handle_event(event):
                    case 'end': 
                        Engd = Post_Game(screen, day_manager.current_day)
                        state = 'post_game'   
                        day_manager.current_day = 1

            case 'post_game':
                match Engd.handle_event(event):
                    case 'exit':
                        running = False
                    case 'home':
                        state = 'home'

            case 'credits':
                match Befg.handle_event(event):
                    case 'home':
                        state = 'home'


    # --- UPDATE --- 
    if state == "in_game":
        match day_manager.is_over():
            case "end":
                Engd = Post_Game(screen, day_manager.current_day)
                state = "post_game"
                day_manager.current_day = 1
            case "continue":
                day_manager.new_day()
        day_manager.update() 
        



    # --- DRAW ---
        screen.fill((0,0,0))
        
    match state:
        case 'home':
            Befg.draw()
        case 'settings':
            Sett.draw()
        case 'in_game':
            Ing.draw(settings.creatures_list, screen)
            day_manager.draw_current_day()
        case 'post_game':
            Engd.draw()

        case 'credits':
            Befg.credits()


    pg.display.flip()
    clock.tick(settings.FPS)
