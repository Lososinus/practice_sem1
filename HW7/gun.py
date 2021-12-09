import math
from random import random 
from random import choice
import pygame.freetype as ft

import pygame


FPS_MAX = 40

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1600
HEIGHT = 900

g = -10

class Ball:
    def __init__(ball, screen: pygame.Surface, x, y, r, vx, vy, resurrection, live):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        ball.screen = screen
        ball.x = x
        ball.y = y
        ball.r = r
        ball.vx = vx
        ball.vy = vy
        ball.color = choice(GAME_COLORS)
        ball.resurrection = resurrection        #POWERWOLF
        ball.live = live                 #оставшееся время жизни в секундах

    def move(ball, g, dt, WIDTH, HEIGHT):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        ball.x  += ball.vx
        ball.y  += ball.vy - g*dt**2/2
        ball.vy -= g*dt
        if ball.vx>0 and ball.x+ball.r>WIDTH:
            ball.vx-= 2.0*ball.vx
        if ball.vy>0 and ball.y+ball.r>HEIGHT:
            ball.vy-= 2.0*ball.vy
        if ball.vx<0 and ball.x-ball.r<0:
            ball.vx-= 2.0*ball.vx
        if ball.vy<0 and ball.y-ball.r<0:
            ball.vy-= 2.0*ball.vy

    def draw(ball):
        pygame.draw.circle(
            ball.screen,
            ball.color,
            (ball.x, ball.y),
            ball.r
        )
    
    def death (ball): #создаёт шрапнель на месте исходного шарика.
        shards = set()
        for i in range (20):
            rand_angl = + 2*math.pi*random()
            rand_v = 10*random()
            shards.add( Ball(screen, ball.x, ball.y, 8, ball.vx + rand_v*math.cos(rand_angl), ball.vy + rand_v*math.sin(rand_angl), False, 0.2 + 0.5*random()) )
        return shards
    
    def hit_test(ball, targ):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (ball.x - targ.x)**2 + (ball.y - targ.y)**2 < (ball.r + targ.r)**2

class Gun:
    def __init__(gun, x, y, screen):
        gun.x = x
        gun.y = y
        gun.screen = screen
        
        gun.power = 20
        gun.on = False
        gun.angl = 0
        gun.color = GREY

    def fire_start(gun, event):
        gun.on = 1

    def targetting(gun, event):
        """Прицеливание. Зависит от положения мыши."""
        gun.angl = math.atan2(event.pos[1]-gun.y, event.pos[0]-gun.x)
    
    def fire_end(gun, event):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(gun.screen, gun.x, gun.y, 15, gun.power * math.cos(gun.angl) * 0.3, gun.power * math.sin(gun.angl) * 0.3, True, 2.0)
        gun.on = 0
        gun.power = 20
        return new_ball
    
    def draw(gun):
        gun_width = 20
        surf_rot = pygame.Surface((gun.power, gun_width))
        pygame.draw.rect(surf_rot, gun.color, (0, 0, gun.power, gun_width))
        pygame.draw.line(surf_rot, MAGENTA, (gun.power-3, 0), (gun.power-6, gun_width), 4)
        surf_rot.set_colorkey((0, 0, 0))
        surf_blit = pygame.transform.rotate(surf_rot, -gun.angl * 180/math.pi)
        surf_blit.set_colorkey((0, 0, 0))
        screen.blit (surf_blit,
         (gun.x - 0.5*(gun.power*abs(math.cos(gun.angl)) + gun_width*abs(math.sin(gun.angl))) + 0.5*gun.power*math.cos(gun.angl),
         gun.y - 0.5*(gun.power*abs(math.sin(gun.angl)) + gun_width*abs(math.cos(gun.angl)))  + 0.5*gun.power*math.sin(gun.angl) 
         )
         )

    def power_up(gun, dt):
        if gun.on:
            gun.power = min (gun.power + 150*dt, 100)
            gun.color = RED
        else:
            gun.power = max (gun.power - 300*dt, 10)
            gun.color = GREY


class Target:
    def __init__(targ, screen, WIDTH, HEIGHT):
        """ Инициализация новой цели. """
        targ.x = WIDTH  * (0.4 + 0.5*random())
        targ.y = HEIGHT * (0.1 + 0.8*random())
        targ.r = 5 + 45*random()
        targ.dir = math.pi  #направление движения
        targ.points = 70 - targ.r #за маленькие больше очков
        targ.live = 1
        targ.color = RED
        targ.screen = screen
    
    def move(targ, dt, WIDTH, HEIGHT):
        targ.dir += 10 * dt * (2.0 * random() - 1.0)
        targ.x += math.cos(targ.dir) * 10 * dt
        targ.y += math.sin(targ.dir) * 10 * dt
        targ.x = min(targ.x, WIDTH)
        targ.x = max(targ.x, 0)
        targ.y = min(targ.y, HEIGHT)
        targ.y = max(targ.y, 0)
    
    def draw(targ):
        pygame.draw.circle (targ.screen, targ.color, (targ.x, targ.y), targ.r)
        pygame.draw.circle (targ.screen, BLACK, (targ.x, targ.y), targ.r, 2)
        pygame.draw.line (targ.screen, CYAN, (targ.x, targ.y), (targ.x + targ.r * math.cos(targ.dir), targ.y + targ.r * math.sin(targ.dir)))


pygame.init()
ft.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
#bullet = 0
balls   = set()
targets = set()
gun_1 = Gun(50, 100, screen)
gun_2 = Gun(50, HEIGHT-100, screen)

clock = pygame.time.Clock()
finished = False
score = 0
fps = 0
while not finished:
    #раздел отрисовки
    screen.fill(WHITE)
    gun_1.draw()
    gun_2.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    font.render_to(screen, (WIDTH - 700, 20), "fps: {0:6.1f} score: {1:5.0f}".format(fps, score), BLACK, (0, 0, 0, 0))
    pygame.display.update()
    
    #получение информации из внешнего мира 
    dt = clock.tick(FPS_MAX) * 0.001
    fps = clock.get_fps()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun_1.fire_start(event)
            gun_2.fire_start(event)
        elif event.type == pygame.MOUSEMOTION:
            gun_1.targetting(event)
            gun_2.targetting(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            balls.add(gun_1.fire_end(event))
            balls.add(gun_2.fire_end(event))
    
    #логика игры
    if random()<dt*5: # добавляет новые цели
        targets.add(Target(screen, WIDTH, HEIGHT))
    for target in targets: 
        target.move(dt, WIDTH, HEIGHT)
    for ball in balls:
        ball.move(g, dt, WIDTH, HEIGHT)
        ball.live = max(ball.live - dt, 0)
        for target in targets:
            if ball.hit_test(target) and target.live:
                target.live = 0
                score += target.points
    
    destroyed = set()
    for target in targets:
        if target.live == 0:
            destroyed.add(target)
    for target in destroyed:
        targets.remove(target)
    
    expired = set()
    for ball in balls:
        if ball.live == 0:
            expired.add(ball)
    for ball in expired:
        if ball.resurrection:
            balls = balls | ball.death()
        balls.remove(ball)
    
    gun_1.power_up(dt)
    gun_2.power_up(dt)

pygame.quit()
