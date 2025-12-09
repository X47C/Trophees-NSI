#  boucle principale -- > execution du programme complet
import pygame as pg
from Pygame.pygame import Before_Game
import settings

running = True
pg.init()
Befg = Before_Game(pg.display.set_mode(settings.Display_size))
Befg.draw()
while running: 
    if Befg.handle_event() == 'left':
        running = False
    if pg.event.peek():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    pg.display.flip()
    pg.time.Clock().tick(60)
