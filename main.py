# I am the main say hello to the new world, rest of the world 'hello, new world'
# the main 'you're great'

import pygame
import time
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock =  pygame.time.Clock()
        self.player = Player(200, 200)
        self.square_area = pygame.Rect(0, 0, 50, 50)
        self.square_area_color = 'red'
        self.coor_mouse = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        self.click1_mouse =  0

    def handling_elt(self):
        for event in pygame.event.get():
            if  not self.coor_mouse == pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1) :
                self.coor_mouse = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1 :
                    if self.square_area.colliderect(self.coor_mouse) :
                        self.click1_mouse = 1





        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.player.velocity[1] = -1
        elif pressed[pygame.K_s]:
            self.player.velocity[1] = 1
        else :
            self.player.velocity[1] = 0

        if pressed[pygame.K_q]:
            self.player.velocity[0] = -1
        elif pressed[pygame.K_d]:
            self.player.velocity[0] = 1
        else :
            self.player.velocity[0] = 0


    def update(self):
        self.player.move()
        if self.click1_mouse == 1:
            self.square_area_color = 'blue'
            self.click1_mouse = 0
        else :
            self.square_area_color = 'red'




    def display(self):
        self.screen.fill('black')
        pygame.draw.rect(self.screen, self.square_area_color, self.square_area)
        self.player.draw(self.screen)
        pygame.display.flip()


    def run(self):
        while self.running :
            self.handling_elt()
            self.update()
            self.display()
            self.clock.tick(30)

class Player :
    def __init__(self, x , y):
        self.image = pygame.image.load("/Users/Glaçier/Documents/testpygamedossier/huohuoversionpti.jpg").convert()
        self.rect = self.image.get_rect(x = x, y = y)
        self.speed = 5
        self.velocity = [0, 0]

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

pygame.init()
screen = pygame.display.set_mode((400,400))
game = Game(screen)
game.run()

pygame.quit()