"""
в данном модуле расположены главные циклы состояний игры - sandbox, saves

класс
    Game_state

функции
    sandbox_loop()
    saves_loop()
"""

from random import random
from random import randint
from time import time_ns
from os import listdir
from math import *
import pygame as pg
import pygame.freetype as ft

from view import *
from input import *
from tree import *
from frame import *
from pcl import *

class Game_state:
    """
    класс в объекте которого хранятся основные параметры и объекты игры - размеры и объект поверхности экрана, настройки, конфигурация кнопок
    """
    FINISHED = 0
    SANDBOX = 1
    SAVES = 2
    HELP = 3

    def __init__(game):
        game.state = Game_state.SANDBOX
        pg.init()
        game.MAX_FPS = 0
        game.WIDTH = 1800
        game.HEIGHT = 1000
        game.SIZE = (game.WIDTH, game.HEIGHT)
        game.screen = pg.display.set_mode(game.SIZE)
        game.clock = pg.time.Clock()
        ft.init()
        game.font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
        game.font.fgcolor = (255, 255, 255, 255)

    def quit(game):
        ft.quit()
        pg.quit()

    #button_start_sprite = pg.image.load("sprites/button_start.png").convert()

def sandbox_loop(game, BACK):
    frame = Frame()
    frame.drag((game.WIDTH / 2, game.HEIGHT / 2))
    frame.flip_y = True
    # загрузка спрайтов
    button_back_sprite = pg.image.load("sprites/button_back.png").convert()
    button_saves_sprite = pg.image.load("sprites/button_saves.png").convert()
    button_add_sprite_0 = pg.image.load("sprites/button_add_0.png").convert()
    button_add_sprite_1 = pg.image.load("sprites/button_add_1.png").convert()
    button_draw_bounds_sprite_0 = game.font.render("Bounds", size = 30, fgcolor = (255, 255, 255, 255))[0]
    button_draw_bounds_sprite_1 = game.font.render("Bounds", size = 30, fgcolor = (0, 200, 0, 255))[0]
    button_draw_r_max_sprite_0 = game.font.render("Rmax", size = 30, fgcolor = (255, 255, 255, 255))[0]
    button_draw_r_max_sprite_1 = game.font.render("Rmax", size = 30, fgcolor = (0, 200, 0, 255))[0]
    button_set_en_0_sprite_0 = game.font.render("set_en_0", size = 30, fgcolor = (255, 255, 255, 255))[0]
    button_cancel_sprite = pg.image.load("sprites/button_cancel.png").convert()
    button_subset_sprite_0 = pg.image.load("sprites/button_subset_0.png").convert()
    button_subset_sprite_1 = pg.image.load("sprites/button_subset_1.png").convert()
    button_draw_lines_sprite_0 = pg.image.load("sprites/draw_lines_0.png").convert()
    # Инициализация элементов интерфейса
    button_screen = Button((20, 50), (1500, 800), sprite_1=Button.get_whitebox_0((1500, 700)))
    button_add = Button((1530, 650), (100, 60), button_add_sprite_0, button_add_sprite_1)
    button_draw_bounds = Button((900, 940), (150, 30), button_draw_bounds_sprite_0, button_draw_bounds_sprite_1)
    button_draw_r_max = Button((1100, 940), (150, 30), button_draw_r_max_sprite_0, button_draw_r_max_sprite_1)
    button_set_en_0 = Button((1100, 860), (150, 30), button_set_en_0_sprite_0)
    buttons = {
        button_screen,
        button_add,
        button_draw_bounds,
        button_draw_r_max,
        button_set_en_0}

    wheel_add_dir = Wheel((1530, 470), (100, 20), 0, 0)
    wheel_add_r   = Wheel((1530, 500), (100, 30), 0, 0)
    wheel_add_g   = Wheel((1530, 550), (100, 30), 0, 0)
    wheel_add_b   = Wheel((1530, 600), (100, 30), 0, 0)
    wheel_screen_x = Wheel(button_screen.pos, button_screen.size, 0, 0, True)
    wheel_screen_y = Wheel(button_screen.pos, button_screen.size, 1, 0, True)
    wheel_timescale = Wheel((500, 950), (300, 30), 0)
    wheel_frame_alph = Wheel((900, 860), (150, 30), 0)
    wheel_vel_scale = Wheel((900, 900), (150, 30), 0)
    wheels = {
        wheel_screen_x,
        wheel_screen_y,
        wheel_timescale,
        wheel_frame_alph,
        wheel_vel_scale,
        wheel_add_r,
        wheel_add_g,
        wheel_add_b,
        wheel_add_dir}
    
    text_m       = Text((1530,  50), (200, 60), game.font, 10, header="mass:",   header_size=25, input_str="1")
    text_r       = Text((1530, 120), (200, 60), game.font, 10, header="radius:", header_size=25, input_str="10")
    text_sigma   = Text((1530, 190), (200, 60), game.font, 10, header="sigm:",   header_size=25, input_str="30")
    text_disp_en = Text((1530, 260), (200, 60), game.font, 10, header="eps:",    header_size=25, input_str="5")
    text_r_max   = Text((1530, 330), (200, 60), game.font, 10, header="r_max:",  header_size=25, input_str="45")
    text_v       = Text((1530, 400), (200, 60), game.font, 10, header="v:",      header_size=25, input_str="0")
    texts = {
        text_m, 
        text_r, 
        text_sigma, 
        text_disp_en, 
        text_r_max, 
        text_v}
    # структуры данных
    gas = set()
    collision_tree = Square_tree()
    interaction_tree = Square_tree()
    # вспомогательные переменные
    fps = 0
    itr = 0
    dt = 0
    timescale = 0.00
    
    pcl_add = Particle_6_12(m=1, x=0, y=0, vx=0, vy=0, r=10, color=(255, 0, 0), disp_en=5, sigma=30, r_max=45)
    pcl_add_v = 0
    pcl_add_v_dir = 0
    draw_add_pcl = False
    
    for i in range(20):
        for k in range(15):
            pcl_add.x = i*30*2**(1/6)
            pcl_add.y = k*30*2**(1/6)
            pcl_new = pcl_add.copy()
            gas.add(pcl_new)
            collision_tree.add_elem(pcl_new.x, pcl_new.y, pcl_new.r, pcl_new)
            interaction_tree.add_elem(pcl_new.x, pcl_new.y, pcl_new.r_max, pcl_new)
    
    interaction_intersect = interaction_tree.get_intersect()
    en_0 = 0
    en = 0
    while game.state == Game_state.SANDBOX:
        for pcl in gas:
            collision_tree.upd_elem(pcl.x, pcl.y, pcl.r, pcl)
            interaction_tree.upd_elem(pcl.x, pcl.y, pcl.r_max, pcl)
        
        collision_intersect = collision_tree.get_intersect()
        for pair in collision_intersect:
            Particle_6_12.calc_coll(pair[0], pair[1])
        
        interaction_intersect = interaction_tree.get_intersect()
        interaction_to_trunc = set()
        for pair in interaction_intersect:
            pcl_1 = pair[0]
            pcl_2 = pair[1]
            if (pcl_1.x - pcl_2.x)**2 + (pcl_1.y - pcl_2.y)**2 > (pcl_1.r_max + pcl_2.r_max)**2:
                interaction_to_trunc.add(pair)
        interaction_intersect = interaction_intersect.difference(interaction_to_trunc)
        Particle_6_12.runge_kutta_6_12(gas, interaction_intersect, dt*timescale)
        
        en = Particle_6_12.calc_energy(gas, interaction_intersect)
        
        if not itr % 10:
            collision_tree.trunc_empty()
            interaction_tree.trunc_empty()
        # отрисовка
        draw_gas(gas, game.screen, frame, wheel_vel_scale.input_tot*0.05, button_draw_r_max.input)
        if draw_add_pcl:
            draw_pcl(pcl_add, game.screen, frame, wheel_vel_scale.input_tot*0.05, True)
        if button_draw_bounds.input:
            for pair in interaction_intersect:
                pcl_1 = pair[0]
                pcl_2 = pair[1]
                pg.draw.line(game.screen, "0x00FF00", frame.direct((pcl_1.x, pcl_1.y)), frame.direct((pcl_2.x, pcl_2.y)))
        
        game.font.render_to(game.screen, (50, 850), "itr:      {0:6d}".format(itr), "0xFFFFFF", (0, 0, 0, 0))
        game.font.render_to(game.screen, (50, 900), "fps:      {0:6.2f}".format(fps), "0xFFFFFF", (0, 0, 0, 0))
        game.font.render_to(game.screen, (50, 950), "timescale:{0:6.2f}".format(timescale), "0xFFFFFF", (0, 0, 0, 0))
        game.font.render_to(game.screen, (500, 850), "n:{0:d}".format(len(gas)), "0xFFFFFF", (0, 0, 0, 0))
        if en_0!=0:
            game.font.render_to(game.screen, (1300, 850), "delta_en/en_0:{0:10.2e}".format(en/en_0-1), "0xFFFFFF", (0, 0, 0, 0), size = 35)
        else:
            game.font.render_to(game.screen, (1300, 850), "delta_en/en_0:        nan", "0xFFFFFF", (0, 0, 0, 0), size = 35)
        game.font.render_to(game.screen, (1300, 900), "en: {0:17.10e}".format(en), "0xFFFFFF", (0, 0, 0, 0), size = 35)
        
        Button.draw_all(buttons, game.screen)
        Wheel.draw_all(wheels, game.screen)
        Text.draw_all(texts, game.screen)
        pg.draw.rect(game.screen, pcl_add.color, (1650, 500, 50, 130))
        pg.draw.rect(game.screen, "0xFFFFFF", (1650, 500, 50, 130), 1)
        
        pg.display.update()
        game.screen.fill("0x000000")
        # Обработка событий
        events = pg.event.get()
        Button.event_handler(buttons, events)
        Wheel.event_handler(wheels, events)
        Text.event_handler(texts, events)
        for event in events:
            if event.type == pg.QUIT:
                game.state = Game_state.FINISHED
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4 and button_screen.above(event.pos):
                    frame.scale_at_point(event.pos, 1.25)
                if event.button == 5 and button_screen.above(event.pos):
                    frame.scale_at_point(event.pos, 0.8)
            elif event.type == pg.MOUSEMOTION:
                draw_add_pcl = button_screen.above(event.pos) and button_add.input
                if button_add.input:
                    pcl_add.x, pcl_add.y = frame.inverse(event.pos)

        timescale = max(0, timescale + wheel_timescale.input * 0.01)
        frame.rotate_around((game.WIDTH / 2, game.HEIGHT / 2), wheel_frame_alph.input * 0.01)
        frame.drag((wheel_screen_x.input, wheel_screen_y.input))
        
        wheel_add_r.input_tot = max(0, min(wheel_add_r.input_tot, 255))
        wheel_add_g.input_tot = max(0, min(wheel_add_g.input_tot, 255))
        wheel_add_b.input_tot = max(0, min(wheel_add_b.input_tot, 255))
        pcl_add.color = (wheel_add_r.input_tot, wheel_add_g.input_tot, wheel_add_b.input_tot)
        if button_add.input:
            pcl_add.m = float(text_m.input)
            pcl_add.vx = float(text_v.input) * cos(wheel_add_dir.input_tot * 0.01)
            pcl_add.vy = float(text_v.input) * sin(wheel_add_dir.input_tot * 0.01)
            pcl_add.r = float(text_r.input)
            pcl_add.disp_en = float(text_disp_en.input)
            pcl_add.sigma = float(text_sigma.input)
            pcl_add.r_max = float(text_r_max.input)
            if button_screen.input:
                pcl_new = pcl_add.copy()
                gas.add(pcl_new)
                collision_tree.add_elem(pcl_new.x, pcl_new.y, pcl_new.r, pcl_new)
                interaction_tree.add_elem(pcl_new.x, pcl_new.y, pcl_new.r_max, pcl_new)
        if button_set_en_0.input:
            en_0 = en
            button_set_en_0.input = False
        for button in buttons:
            button.input_prev = button.input
        
        button_screen.input = False
        dt = game.clock.tick(game.MAX_FPS) / 1000
        fps = game.clock.get_fps()
        
        
        itr += 1

if __name__ == "__main__":
    print("This module is not for direct call!")
