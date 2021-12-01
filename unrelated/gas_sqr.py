from random import random
from random import randint
import pygame as pg
import pygame.freetype as ft
import numpy as np


class Particle:
    def __init__(self, m=1, r=10, color=(0, 0, 0), x=0, y=0, vx=0, vy=0):
        self.m = m
        self.r = r
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def coll_pcl(pcl_1, pcl_2):
        scl_sqr_dr = (pcl_1.x - pcl_2.x)**2 + (pcl_1.y - pcl_2.y)**2
        if scl_sqr_dr < (pcl_1.r + pcl_2.r)**2:
            dr_dot_dv = (pcl_1.vx-pcl_2.vx)*(pcl_1.x-pcl_2.x) + (pcl_1.vy-pcl_2.vy)*(pcl_1.y-pcl_2.y)
            if dr_dot_dv < 0:
                common_factor  = 2.0*dr_dot_dv/((pcl_1.m + pcl_2.m) * scl_sqr_dr)
                pcl_1.vx -= pcl_2.m * (pcl_1.x - pcl_2.x) * common_factor
                pcl_1.vy -= pcl_2.m * (pcl_1.y - pcl_2.y) * common_factor
                pcl_2.vx -= pcl_1.m * (pcl_2.x - pcl_1.x) * common_factor
                pcl_2.vy -= pcl_1.m * (pcl_2.y - pcl_1.y) * common_factor
	
    def coll_segm(self, x1, y1, x2, y2):
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

    def move_dt(self, dt, g):
        # обрабатывает итерацию движения частицы за dt
        self.x+= self.vx*dt
        self.y+= self.vy*dt - 0.5*g*dt**2
        self.vy-= g*dt

    def draw_pcl(self, surf):
        pg.draw.circle (surf, self.color, (round(self.x), round(self.y)), round(self.r))
        pg.draw.circle (surf, (200, 200, 200), (round(self.x), round(self.y)), round(self.r), 1)

class Button:
    pg.init()
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
        if (self.x < x_click) & (self.x + self.w > x_click) & (self.y < y_click) & (self.y + self.h > y_click):
            self.state = not self.state
    
    def draw_butt (self, surface):
        if self.state:
            if (self.w, self.h) != self.sprite_1.get_size():
                self.sprite_1 = pg.transform.smoothscale(self.sprite_1, (self.w, self.h))
            surface.blit(self.sprite_1, (self.x, self.y))
        else:
            if (self.w, self.h) != self.sprite_0.get_size():
                self.sprite_0 = pg.transform.smoothscale(self.sprite_0, (self.w, self.h)) 
            surface.blit(self.sprite_0, (self.x, self.y))

class Square_tree:
    def __init__ (root, parent, x, y, l):
        root.parent = parent
        root.child_lu = None
        root.child_ru = None
        root.child_rd = None
        root.child_ld = None
        root.gas = set()
        root.total_amm=0
        root.x = x
        root.y = y
        root.l = l #координаты центра и полусторона
    
    @staticmethod
    def intersection_check(l, x, y, r):
        x_mns_l = x-l
        x_pls_l = x+l
        y_mns_l = y-l
        y_pls_l = y+l
        return y-l<r and x-l<r and y+l>-r and x+l>-r and (x<l and x>-l or y<l and y>-l or (x+l)**2+(y+l)**2<r**2 or (x-l)**2+(y+l)**2<r**2 or (x-l)**2+(y-l)**2<r**2 or (x+l)**2+(y-l)**2<r**2)
    
    def add_pcl_handler(root, pcl, min_l):
        root.total_amm+=1
        if root.l < min_l*2:
            root.gas.add(pcl)
        else:
            if pcl.x-root.x<pcl.r and pcl.y-root.y<pcl.r:
            #if Square_tree.intersection_check(root.l/2, pcl.x-(root.x-root.l/2), pcl.y-(root.y-root.l/2), pcl.r):
                if root.child_lu is None:
                    root.child_lu = Square_tree(root, root.x-root.l/2, root.y-root.l/2, root.l/2)
                root.child_lu.add_pcl_handler(pcl, min_l)
            
            if pcl.x-root.x>-pcl.r and pcl.y-root.y<pcl.r:
            #if Square_tree.intersection_check(root.l/2, pcl.x-(root.x+root.l/2), pcl.y-(root.y-root.l/2), pcl.r):
                if root.child_ru is None:
                    root.child_ru = Square_tree(root, root.x+root.l/2, root.y-root.l/2, root.l/2)
                root.child_ru.add_pcl_handler(pcl, min_l)
            
            if pcl.x-root.x>-pcl.r and pcl.y-root.y>-pcl.r:
            #if Square_tree.intersection_check(root.l/2, pcl.x-(root.x+root.l/2), pcl.y-(root.y+root.l/2), pcl.r):
                if root.child_rd is None:
                    root.child_rd = Square_tree(root, root.x+root.l/2, root.y+root.l/2, root.l/2)
                root.child_rd.add_pcl_handler(pcl, min_l)
            
            if pcl.x-root.x<pcl.r and pcl.y-root.y>-pcl.r:
            #if Square_tree.intersection_check(root.l/2, pcl.x-(root.x-root.l/2), pcl.y-(root.y+root.l/2), pcl.r):
                if root.child_ld is None:
                    root.child_ld = Square_tree(root, root.x-root.l/2, root.y+root.l/2, root.l/2)
                root.child_ld.add_pcl_handler(pcl, min_l)
        
    def add_pcl(root, pcl):
        if Square_tree.intersection_check(root.l, pcl.x-root.x, pcl.y-root.y, pcl.r):
            root.add_pcl_handler(pcl, pcl.r*1.0)
    
    def draw_sqr_tree (root, screen):
        if root.gas:
            screen.fill ((40, 130, 200), (root.x-root.l, root.y-root.l, 2*root.l, 2*root.l))
        pg.draw.rect (screen, (200, 200, 200), (root.x-root.l, root.y-root.l, 2*root.l, 2*root.l), 1)
        if root.child_lu is not None and root.child_lu.total_amm != 0:
            root.child_lu.draw_sqr_tree(screen)
        if root.child_ru is not None and root.child_ru.total_amm != 0:
            root.child_ru.draw_sqr_tree(screen)
        if root.child_rd is not None and root.child_rd.total_amm != 0:
            root.child_rd.draw_sqr_tree(screen)
        if root.child_ld is not None and root.child_ld.total_amm != 0:
            root.child_ld.draw_sqr_tree(screen)
    
    
    def coll (root):
        sub_gas_lu, intersect_lu = root.child_lu.coll() if root.child_lu is not None and root.child_lu.total_amm != 0 else (set(), set())
        sub_gas_ru, intersect_ru = root.child_ru.coll() if root.child_ru is not None and root.child_ru.total_amm != 0 else (set(), set())
        sub_gas_rd, intersect_rd = root.child_rd.coll() if root.child_rd is not None and root.child_rd.total_amm != 0 else (set(), set())
        sub_gas_ld, intersect_ld = root.child_ld.coll() if root.child_ld is not None and root.child_ld.total_amm != 0 else (set(), set())
        
        intersect = intersect_lu | intersect_ru | intersect_rd | intersect_ld
        sub_gas = root.gas | sub_gas_lu | sub_gas_ru | sub_gas_rd | sub_gas_ld
        for pcl_1 in root.gas:
            for pcl_2 in sub_gas:
                if pcl_1 is not pcl_2:
                    intersect.add((pcl_1, pcl_2))
        return sub_gas, intersect;
    
    def tree_intersect(root):
        return root.coll()[1]

# константы
max_fps = 50
width = 1024
hight = 512
g = -0
f_forward = 0.10
# стенки
walls = set()
#walls.add((width*0.00, hight*0.00, width*0.50, hight*1.00))
#walls.add((width*1.00, hight*0.00, width*0.50, hight*1.00))
# инициализация газа
n = 5000
gas = set()
for i in range(n):
	gas.add(Particle(m=1, r=4.0, color=(150, 30, 150), x=(0.10+0.80*random())*width, y=(0.10+0.80*random())*hight, vx=100*(-1.00+2.00*random()), vy=100*(-1.00+2.00*random())))
#gas.add(Particle(m=1000, r=40, color=(150, 30, 150), x=(0.70+0.00*random())*width, y=(0.50+0.00*random())*hight, vx=400*(-1.00+2.00*random()), vy=400*(-1.00+2.00*random())))
root = Square_tree(None, width/2, hight/2, max(width/2, hight/2))
for pcl in gas:
    root.add_pcl(pcl)
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((width, hight+200))
clock = pg.time.Clock()
subclock = pg.time.Clock()
subclock_1 = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
# кнопки
btn_1 = Button(550, hight+50, 150, 100)
btn_spinc = Button(800, hight+50, 50, 50)
btn_spdec = Button(750, hight+50, 50, 50)
# осн цикл
'''
av_len = 1000
av_line = [0] * av_len
av_i = 0
av_sum = 0
    av_sum -= av_line[av_i]
    av_line[av_i] = dt
    av_sum += av_line[av_i]
    av_i = (av_i + 1)%av_len
'''
delta_t = 0
dt_draw = 0
dt_compute = 0
dt_write = 0
dt_1 = 0
dt_2 = 0
dt_3 = 0
fps = 0
itr = 0
dt = 0
while not finished:
    if btn_spinc.state:
        f_forward += 0.02
        btn_spinc.state = False
    if btn_spdec.state:
        f_forward = max(f_forward-0.02, 0)
        btn_spdec.state = False
    subclock.tick()
    
    for pcl in gas:
        pcl.move_dt(dt*f_forward, g)
        for wall in walls:
            pcl.coll_segm(wall[0], wall[1], wall[2], wall[3])
        if pcl.vx>0 and pcl.x+pcl.r>width:
            pcl.vx-= 2.0*pcl.vx
        if pcl.vy>0 and pcl.y+pcl.r>hight:
            pcl.vy-= 2.0*pcl.vy
        if pcl.vx<0 and pcl.x-pcl.r<0:
            pcl.vx-= 2.0*pcl.vx
        if pcl.vy<0 and pcl.y-pcl.r<0:
            pcl.vy-= 2.0*pcl.vy
    subclock_1.tick()
    
    root = Square_tree(None, width/2, hight/2, max(width/2, hight/2))
    for pcl in gas:
        root.add_pcl(pcl)
    dt_1 = subclock_1.tick()
    
    intersect = root.tree_intersect()
    dt_2 = subclock_1.tick()
    
    for pair in intersect:
        Particle.coll_pcl(pair[0], pair[1])
    dt_3 = subclock_1.tick()
    
    dt_compute = subclock.tick()
    
    if btn_1.state:
        root.draw_sqr_tree(screen)
    gas_surf = pg.Surface((width, hight))
    for pcl in gas:
        pcl.draw_pcl(gas_surf)
    gas_surf.set_alpha(150)
    gas_surf.set_colorkey((0, 0, 0))
    screen.blit(gas_surf, (0, 0))
    for wall in walls:
        pg.draw.line(screen, (255, 0, 255), (round(wall[0]), round(wall[1])), (round(wall[2]), round(wall[3])))
    dt_draw = subclock.tick()
    
    print ("{0:5d} {1:5d} {2:5d} {3:5d} {4:5d}".format(len(intersect), dt_compute, dt_1, dt_2, dt_3))
    font.render_to(screen, (10, hight+50*0), "fps:      {0:6.2f}   itr:{1:4d}   n:{2:4d}".format(fps, itr, n), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*1), "dt_compute: {0:4d}".format(dt_compute), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*2), "dt_draw:    {0:4d}".format(dt_draw   ), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*3), "f_forward:{0:4.2f}".format(f_forward ), (232, 98, 129), (0, 0, 0))
    btn_1.draw_butt(screen)
    btn_spinc.draw_butt(screen)
    btn_spdec.draw_butt(screen)
    dt_write = subclock.tick()
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, width, hight+200))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            btn_1.click(event.pos[0], event.pos[1])
            btn_spinc.click(event.pos[0], event.pos[1])
            btn_spdec.click(event.pos[0], event.pos[1])
    
    delta_t = clock.tick(max_fps)
    dt = delta_t/1000
    fps = clock.get_fps()
    itr+=1
	
ft.quit()
pg.quit()
