from random import random
from random import randint
from time import time_ns as nanosec #потому что могу
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
time_step = 1.0
max_fps = 30
width = 1600
hight = 800
gm = 2000
x_grav = width/2
y_grav = hight + 100
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((width, hight+200))
clock = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
# инициализация газа
n = 800
gas = set()
for i in range(n):
    gas.add( Particle(m=1, r=2.0, color=(150,  20,  20), x=700+200*random(), y=500, vx=0, vy=0) )
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
fps = 0
itr = 0
pcl_0 = Particle(m=1E20, r=50, color=(150, 30, 150), x=x_grav, y=y_grav, vx=0, vy=0)
tree.add_pcl(pcl_0)

en_0 = 0
for pcl in gas:
    en_0 += pcl.m*(pcl.vx**2 + pcl.vy**2)*0.5 - pcl.m*gm / ((pcl.x-x_grav)**2 + (pcl.y-y_grav)**2)**0.5
en_prev = en_0

gas_trace = pg.Surface((width, hight))
while not finished:
    if btn_spinc.state:
        time_step += 0.1
        btn_spinc.state = False
    if btn_spdec.state:
        time_step = max(time_step-0.1, 0)
        btn_spdec.state = False
    
    t0 = nanosec()
    for pcl in gas:
        for k in range(10):
            pcl.runge_kutta(time_step/10, gm, x_grav, y_grav)
    dt_grav = (nanosec()-t0)//1000000
    
    t1 = nanosec()
    for pcl in gas:
        if pcl.vx>0 and pcl.x+pcl.r>width:
            pcl.vx-= 2.0*pcl.vx
        if pcl.vy>0 and pcl.y+pcl.r>hight:
            pcl.vy-= 2.0*pcl.vy
        if pcl.vx<0 and pcl.x-pcl.r<0:
            pcl.vx-= 2.0*pcl.vx
        if pcl.vy<0 and pcl.y-pcl.r<0:
            pcl.vy-= 2.0*pcl.vy
    
    for pcl in gas:
        tree.upd_pcl(pcl)
    intersect = tree.get_intersect()
    for pair in intersect:
        Particle.coll_pcl(pair[0], pair[1])
    
    dt_coll = (nanosec()-t1)//1000000
    
    print()
    en = 0
    for pcl in gas:
	    en += pcl.m*(pcl.vx**2 + pcl.vy**2)*0.5 - pcl.m*gm / ((pcl.x-x_grav)**2 + (pcl.y-y_grav)**2)**0.5
    print ("{0:+6.2f} {1:+6.2f}".format(np.log(np.abs(en/en_0-1))/np.log(10), np.log(np.abs(en/en_prev-1))/np.log(10)))
    en_prev = en
    
    font.render_to(screen, (10, hight+50*0), "fps:      {0:6.2f}   itr:{1:4d}                         n:{2:4d}".format(fps, itr, n), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*1), "dt_grav:  {0:6d}  ".format(dt_grav), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*2), "dt_coll:  {0:6d}  ".format(dt_coll), (232, 98, 129), (0, 0, 0))
    font.render_to(screen, (10, hight+50*3), "timestep: {0:6.2f}".format(time_step), (232, 98, 129), (0, 0, 0))
    
    if btn_1.state:
        tree.root.draw_root(screen)
    
    gas_trace.set_alpha(0)
    gas_surf = pg.Surface((width, hight))
    gas_surf.blit(gas_trace, (0, 0))
    gas_surf.set_colorkey((0, 0, 0))
    gas_surf.set_alpha(230)
    for pcl in gas:
        pcl.draw_pcl(gas_surf)
    pcl_0.draw_pcl(screen)
    screen.blit(gas_surf, (0, 0))
    gas_trace = gas_surf
    
    font.render_to(screen, (10, hight+50*0), "", (232, 98, 129), (0, 0, 0))
    btn_1.draw_butt(screen)
    btn_spinc.draw_butt(screen)
    btn_spdec.draw_butt(screen)
    
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
    fps = clock.get_fps()
    itr+=1
	
ft.quit()
pg.quit()
