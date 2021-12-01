from random import random
from random import randint
import pygame as pg
import pygame.freetype as ft

class Particle:
	# Простая частица в форме круга
    def __init__(self, m=1, r=10, color=(0, 0, 0), x=0, y=0, vx=0, vy=0):
        self.m = m
        self.r = r
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    @staticmethod
    def sweep_and_prune(gas, wx, wy):
        #возвращает множество пар - номера частиц чьи проекции на прямую с направляющим вектором (wx, wy) пересекаются.
        segm = [(0,0,None)] * len(gas)
        i = 0
        for pcl in gas:
            proj = pcl.x*wx+pcl.y*wy
            #segm[i] = (proj-r[i], proj+r[i], pcl)
            i+=1
        segm.sort()

        intersect = set()
        for i in range(len(gas)-1):
            k=i+1
            while (k<len(gas) and segm[i][1]>segm[k][0]):
                intersect.add( (segm[i][2], segm[k][2]) )
                k+=1
        return intersect
    
    def coll_pcl(pcl_1, pcl_2):
    	#Расчёт скоростей после упругого столкновени 2 частиц. Включает проверку на пересечение и сближение.
        scl_sqr_dr = (pcl_1.x - pcl_2.x)**2 + (pcl_1.y - pcl_2.y)**2
        if scl_sqr_dr < (pcl_1.r + pcl_2.r)**2:
            dr_dot_dv = (pcl_1.vx-pcl_2.vx)*(pcl_1.x-pcl_2.x) + (pcl_1.vy-pcl_2.vy)*(pcl_1.y-pcl_2.y)
            if dr_dot_dv < 0:
                common_factor  = 2.0*dr_dot_dv/((pcl_1.m + pcl_2.m) * scl_sqr_dr)
                pcl_1.vx -= pcl_2.m * (pcl_1.x - pcl_2.x) * common_factor
                pcl_1.vy -= pcl_2.m * (pcl_1.y - pcl_2.y) * common_factor
                pcl_2.vx -= pcl_1.m * (pcl_2.x - pcl_1.x) * common_factor
                pcl_2.vy -= pcl_1.m * (pcl_2.y - pcl_1.y) * common_factor
            return 1
        else:
            return 0
    '''
    def coll_segm(self, x1, y1, x2, y2):
        #упругое столкновение с неподвижным отрезком с задаными концами
        x1 -= self.x
        y1 -= self.y
        x2 -= self.x
        y2 -= self.y
        cross_div_delta = (x1*y2 - y1*x2)/((x1-x2)**2 + (y1-y2)**2)
        norm_x = cross_div_delta * (y2-y1)
        norm_y = cross_div_delta * (x1-x2)
        scl_sqr_norm = norm_x**2 + norm_y**2
        if scl_sqr_norm < self.r**2:
            scl_sqr1 = x1*x1 + y1*y1
            scl_sqr2 = x2*x2 + y2*y2
            dot_prod = x1*x2 + y1*y2
            if (scl_sqr1-dot_prod) * (scl_sqr2-dot_prod) > 0:
                if norm_x*self.vx + norm_y*self.vy > 0:
                    proj_factor = 2.0*(norm_x*self.vx + norm_y*self.vy) / scl_sqr_norm
                    self.vx -= norm_x * proj_factor
                    self.vy -= norm_y * proj_factor
            elif scl_sqr1 < scl_sqr2:
                if (scl_sqr1 < self.r**2) and (x1*self.vx + y1*self.vy > 0):
                    proj_factor = 2.0*(x1*self.vx + y1*self.vy) / scl_sqr1
                    self.vx -= x1 * proj_factor
                    self.vy -= y1 * proj_factor
            else:
                if (scl_sqr2 < self.r**2) and (x2*self.vx + y2*self.vy > 0):
                    proj_factor = 2.0*(x2*self.vx + y2*self.vy) / scl_sqr2
                    self.vx -= x2 * proj_factor
                    self.vy -= y2 * proj_factor
    '''
    def move_dt(self, dt, g):
        #итерация перемещения частицы в поле тяжести
        self.x+= self.vx*dt
        self.y+= self.vy*dt - 0.5*g*dt**2
        self.vy-= g*dt

    def draw_pcl(self, surf):
        #рисует частицу на поверхности surf
        pg.draw.circle (surf, self.color, (round(self.x), round(self.y)), round(self.r))
        pg.draw.circle (surf, (200, 200, 200), (round(self.x), round(self.y)), round(self.r), 1)

class Button:
	#белые коробки - спрайты по умолчанию
    whitebox_0 = pg.Surface((200, 200))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 0), (199, 0))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 0), (199, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 199), (0, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 199), (0, 0))
    whitebox_1 = whitebox_0.copy()
    pg.draw.line(whitebox_1, (200, 200, 200), (0, 0), (199, 199))
    pg.draw.line(whitebox_1, (200, 200, 200), (199, 0), (0, 199))
    
    def __init__ (self, x, y, w, h, sprite_0 = whitebox_0, sprite_1 = whitebox_1, state = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sprite_0 = sprite_0
        self.sprite_1 = sprite_1
        self.state = state
    
    def click (self, x_click, y_click):
    	#меняет состояние при попадании по кнопке
        if (self.x < x_click) & (self.x + self.w > x_click) & (self.y < y_click) & (self.y + self.h > y_click):
            self.state = not self.state
    
    def draw_butt (self, surface):
    	#в зависимости от состояния рисует нужный спрайт
        if self.state:
            if (self.w, self.h) != self.sprite_1.get_size():
                self.sprite_1 = pg.transform.smoothscale(self.sprite_1, (self.w, self.h))
            surface.blit(self.sprite_1, (self.x, self.y))
        else:
            if (self.w, self.h) != self.sprite_0.get_size():
                self.sprite_0 = pg.transform.smoothscale(self.sprite_0, (self.w, self.h)) 
            surface.blit(self.sprite_0, (self.x, self.y))


# константы
MAX_FPS = 40
WIDTH = 1600
HIGHT = 800
GAME_T = 20000 #время раунда в мс
FONT_COLOR = (200, 100, 200)
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((WIDTH, HIGHT))
clock = pg.time.Clock()
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)

# осн циклы - начала игры, игра, ввод имени.
delta_t = 0
fps = 0
itr = 0
dt = 0
started  = False
finished = False
named  = False
while not started:
    font.render_to(screen, (200, 300), "press _space_ to start".format(), FONT_COLOR, (0, 0, 0))
	    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            started  = True
            finished = True
            named  = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                started  = True
    
    fps = clock.get_fps()


t0 = pg.time.get_ticks()
x_lol, y_lol  = 0, 0
score = 0
while not finished:
    font.render_to(screen, (5, 5 + 60*0), "gaming is happening".format(), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (5, 5 + 60*1), "FPS: {0:5.2f}".format(fps), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (5, 5 + 60*2), "Time left: {0:5.1f}".format( (GAME_T - (pg.time.get_ticks() - t0))/1000 ), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (5, 5 + 60*3), "Score: {0:d}".format(score), FONT_COLOR, (0, 0, 0))
    
    pg.draw.circle(screen, (200, 200, 200), (round(x_lol), round(y_lol)), round(5), 1)
    
    pg.display.update()
    screen.fill((0, 0, 0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            started  = True
            finished = True
            named  = True
    
    clock.tick(MAX_FPS)
    fps = clock.get_fps()
    finished = finished or pg.time.get_ticks() - t0 > GAME_T

skipped = False
player_name = ""
pg.key.start_text_input()
while not named:
    font.render_to(screen, (200, 200), "Score: {0:d}".format(score), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (200, 250), "Enter name then _enter_".format(), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (200, 300), "or press _esc_ to skip".format(), FONT_COLOR, (0, 0, 0))
    font.render_to(screen, (200, 400), player_name + "_", FONT_COLOR, (0, 0, 0))
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            started  = True
            finished = True
            named  = True
        elif event.type == pg.TEXTINPUT:
            player_name += event.text
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                player_name = player_name[0:len(player_name)-1]
            elif event.key == pg.K_ESCAPE:
                named  = True
                skipped = True
    clock.tick(MAX_FPS)
    fps = clock.get_fps()
    
if not skipped:
    pass

ft.quit()
pg.quit()
