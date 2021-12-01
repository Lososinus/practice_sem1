from random import random
from random import randint
from time import time_ns as nanosec
import pygame as pg
import pygame.freetype as ft
import numpy as np
from btn import *
from pcl import *
from tree import *

        
def draw_root (root, screen):
    if root.light:# or True:
        if len(root.gas)!=0:
            screen.fill ((40, 130, 200), (root.x-root.r, root.y-root.r, 2*root.r, 2*root.r))
        pg.draw.rect (screen, (200, 200, 200), (root.x-root.r, root.y-root.r, root.r*2, root.r*2), 1)
        if root.child_lu is not None:
            root.child_lu.draw_root(screen)
        if root.child_ru is not None:
            root.child_ru.draw_root(screen)
        if root.child_rd is not None:
            root.child_rd.draw_root(screen)
        if root.child_ld is not None:
            root.child_ld.draw_root(screen)

Tree_root.draw_root = draw_root
del draw_root

# константы
max_fps = 40
width = 1000
hight = 800
g = -0
f_forward = 0.20
# стенки
walls = set()
#walls.add((width*0.00, hight*0.00, width*0.50, hight*1.00))
#walls.add((width*1.00, hight*0.00, width*0.50, hight*1.00))
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((width, hight+200))
clock = pg.time.Clock()
subclock = pg.time.Clock()
subclock_1 = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
# инициализация газа
n = 3000
gas = set()
'''
for i in range(n):
    gas.add(Particle(m=1, r=3.0, color=(100, 100, 200), x=width, y=(0.01+0.98*random())*hight, vx=-1000, vy=0))
'''
pcl_big = Particle(m=1E7, r=40.0, color=(180, 30, 40), x=(0.60+0.00*random())*width, y=(0.50+0.00*random())*hight, vx=0, vy=0) 

gas.add( pcl_big )
tree = Square_tree()
for pcl in gas:
    tree.add_pcl(pcl)
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

gas_trace = pg.Surface((width, hight))
t0 = nanosec()
tot_amm = 0
while not finished:
    if btn_spinc.state:
        f_forward += 0.05
        btn_spinc.state = False
    if btn_spdec.state:
        f_forward = max(f_forward-0.04, 0)
        btn_spdec.state = False
    subclock.tick()

    gas_flown = set()
    for pcl in gas:
        pcl.move_dt(dt*f_forward, g)
        if pcl.vx>0 and pcl.x+pcl.r>width:
            pcl.vx-= 2.0*pcl.vx
        if pcl.vy>0 and pcl.y+pcl.r>hight:
        	gas_flown.add(pcl)
            #pcl.vy-= 2.0*pcl.vy
        if pcl.vx<0 and pcl.x-pcl.r<0:
        	gas_flown.add(pcl)
            #pcl.vx-= 2.0*pcl.vx
        if pcl.vy<0 and pcl.y-pcl.r<0:
        	gas_flown.add(pcl)
            #pcl.vy-= 2.0*pcl.vy
    for pcl in gas_flown:
	    gas.remove(pcl)
	    tree.del_pcl(pcl)

    while tot_amm < (nanosec() - t0)*1E-9*300:
        tot_amm += 1
        pcl_new = Particle(m=1, r=5.0, color=(100, 100, 200), x=width, y=(0.2+0.6*random())*hight, vx=-1000 + 00*(2*random()-1), vy=00*(2*random()-1))
        gas.add(pcl_new)
        tree.add_pcl(pcl_new)
    n = len(gas)
    	
    subclock_1.tick()
    for pcl in gas:
        tree.upd_pcl(pcl)
    dt_1 = subclock_1.tick()
    
    intersect = tree.get_intersect()
    dt_2 = subclock_1.tick()
    
    coll_amm = 0
    for pair in intersect:
        coll_amm += Particle.coll_pcl(pair[0], pair[1])
    dt_3 = subclock_1.tick()
    
    dt_compute = subclock.tick()
    
    if btn_1.state:
        tree.root.draw_root(screen)
    
    gas_trace.set_alpha(0)
    gas_surf = pg.Surface((width, hight))
    gas_surf.blit(gas_trace, (0, 0))
    gas_surf.set_colorkey((0, 0, 0))
    gas_surf.set_alpha(100)
    for pcl in gas:
        pcl.draw_pcl(gas_surf)
    screen.blit(gas_surf, (0, 0))
    gas_trace = gas_surf.copy()
    
    for wall in walls:
        pg.draw.line(screen, (255, 0, 255), (round(wall[0]), round(wall[1])), (round(wall[2]), round(wall[3])))
    
    dt_draw = subclock.tick()
    
    #print ("{0:5d} {1:5d} {2:5d} {3:5d} {4:5d}".format(len(intersect), coll_amm, dt_1, dt_2, dt_3))
    print (pcl_big.vx)
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
