#  boucle principale 
import pygame as pg
from Pygame.pygame import Before_Game, Settings, In_Game, Post_Game
import settings
from Game.game import Day_Manager
from Pygame.food_editor import food_editor


# --- INIT ---

pg.init()
pg.display.set_caption('Darwined')

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
                        Sett.editable_button_set_value()
                    case 'exit':
                        running = False
                    case 'credits':
                        state = 'credits'

            case 'settings':
                Sett.editable_button_refresh(event)
                match Sett.handle_event(event):
                    case'start':
                        day_manager.first_day()
                        settings.toolbox_show_day = True
                        settings.toolbox_show_creatures = True
                        settings.toolbox_show_food = True
                        settings.toolbox_show_vision = True
                        settings.toolbox_simulation_speed = 1
                        Ing.toolbox.open = False
                        state = 'in_game'
                    case 'back':
                        state = 'home'
                    case 'edit_food_curve':
                        editor = food_editor(screen)
                        state = 'edit_food_curve'

            case 'edit_food_curve':
                match editor.handle_event(event):
                    case 'settings':
                        state = 'settings'

            case 'in_game':
                if len(settings.creatures_list) == 0:
                    state = 'post_game'
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
        speed = getattr(settings, 'toolbox_simulation_speed', 1)
        if speed == 0.5:
            if not hasattr(day_manager, '_slow_tick'):
                day_manager._slow_tick = 0
            day_manager._slow_tick += 1
            if day_manager._slow_tick % 2 == 0:
                day_manager.update()
        else:
            updates = int(speed) 
            for _ in range(updates):
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
            day_manager.draw_creature_number()
            day_manager.draw_food_number()
        case 'post_game':
            Engd.draw()
        case 'credits':
            Befg.credits()
        case 'edit_food_curve':
            editor.draw()


    
    pg.display.flip()
    clock.tick(settings.FPS)

