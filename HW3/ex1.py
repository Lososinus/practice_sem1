import pygame
from pygame.draw import *
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
polygon(screen, (255, 255, 255), [(0,0), (400,0),
                               (400,400), (0,400)])

circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 1)

circle(screen, (255, 0, 0), (230, 170), 10)
circle(screen, (0, 0, 0), (230, 170), 5)
circle(screen, (255, 0, 0), (170, 170), 15)
circle(screen, (0, 0, 0), (170, 170), 5)

polygon(screen, (0, 0, 0), [(180,170), (185,165),
                               (110,90), (105,95)])
polygon(screen, (0, 0, 0), [(220,170), (215,165),
                               (290,90), (295,95)])
polygon(screen, (0, 0, 0), [(160,260), (240,260),
                               (240,250), (160,250)])

#arc(screen, (255, 255, 255), (100, 100, 50, 50), 0, 1, 1)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()