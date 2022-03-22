from frame import *
import pygame as pg

"""
в этом модуле находятся функции для рисования объектов
с помощью pygame

функции:
    
    draw_bodies(bodies: set, surf: pygame.Surface, frame: Frame, drawlines: bool):
        рисует данное множество тел
    draw_pseudobody(part_set: set, vx: float, vy: float, surf: pygame.Surface, frame: Frame):
        рисует множество деталей и вектор скорости от одной из них
"""

def draw_bodies(bodies, surf, frame, drawlines = True):
    """
    рисует данное множество тел
    
    **bodies** - множество тел
    **surf** - поверхность для рисования
    **frame** - мировая система отсчёта в экранной
    **drawlines** - рисовать ли линии от деталей к ЦМ
    """
    for body in bodies:
        for part in body.part:
            if drawlines:
                pg.draw.line (surf, "0x00D0D0", frame.direct((part.x, part.y)), frame.direct((body.x, body.y)) )
            pg.draw.circle (surf, "0xD0D0D0", frame.direct((part.x, part.y)), round(part.r * frame.scale), 1)
    for body in bodies:
        for part in body.part:
            pg.draw.circle(surf, part.color, frame.direct((part.x, part.y)), round(part.r * frame.scale - 1))
    for body in bodies:
        body_screen_x, body_screen_y = frame.direct((body.x, body.y))
        icon_size = 10
        if icon_size != 0:
            pg.draw.lines (surf, "0x00D0D0", True, [(body_screen_x, body_screen_y + icon_size), (body_screen_x + icon_size, body_screen_y), (body_screen_x, body_screen_y - icon_size), (body_screen_x - icon_size, body_screen_y)])
            
def draw_pseudobody(part_set, vx, vy, surf, frame):
    """
    рисует множество деталей и вектор скорости от одной из них.
    для визуализации создаваемого тела перед добавлением
    
    **part_set** - множество деталей
    **vx** - скорость по x
    **vy** - скорость по y
    **surf** - поверхность для рисования
    **frame** - мировая система отсчёта в экранной
    """
    for part in part_set:
        pg.draw.circle (surf, "0xD0D0D0", frame.direct((part.x, part.y)), round(part.r * frame.scale), 1)
    for part in part_set:
        pg.draw.circle(surf, part.color, frame.direct((part.x, part.y)), round(part.r * frame.scale - 1))
    if len(part_set):
        some_part = next(iter(part_set))
        part_screen_x, part_screen_y = frame.direct( (some_part.x, some_part.y) )
        part_screen_x_1, part_screen_y_1 = frame.direct( (some_part.x + vx, some_part.y + vy) )
        pg.draw.line (surf, "0x00D0D0", (part_screen_x, part_screen_y), (part_screen_x_1, part_screen_y_1))

def draw_gas(gas, surf, frame, vel_scale, draw_r_max):
    for pcl in gas:
        pg.draw.circle (surf, "0x909090", frame.direct((pcl.x, pcl.y)), pcl.sigma*frame.scale*2**(1/6), 1)
    for pcl in gas:
        pg.draw.circle (surf, pcl.color, frame.direct((pcl.x, pcl.y)), pcl.r*frame.scale)
        pg.draw.circle (surf, "0xFFFFFF", frame.direct((pcl.x, pcl.y)), pcl.r*frame.scale, 1)
    if draw_r_max:
        for pcl in gas:
            pg.draw.circle (surf, (100, 250, 100), frame.direct((pcl.x, pcl.y)), pcl.r_max*frame.scale, 1)
    for pcl in gas:
        pg.draw.line(surf, "0xFFFFFF", frame.direct((pcl.x, pcl.y)), frame.direct((pcl.x + pcl.vx*vel_scale, pcl.y + pcl.vy*vel_scale)))

def draw_pcl(pcl, surf, frame, vel_scale, draw_r_max):
    #рисует частицу на поверхности surf
    screen_pos = frame.direct((pcl.x, pcl.y))
    pg.draw.circle (surf, pcl.color, screen_pos, pcl.r*frame.scale)
    pg.draw.circle (surf, "0x909090", screen_pos, pcl.sigma*frame.scale*2**(1/6), 1)
    pg.draw.circle (surf, "0xFFFFFF", screen_pos, pcl.r*frame.scale, 1)
    if draw_r_max:
        pg.draw.circle (surf, (100, 250, 100), screen_pos, pcl.r_max*frame.scale, 1)
    pg.draw.line(surf, "0xFFFFFF", screen_pos, frame.direct((pcl.x + pcl.vx*vel_scale, pcl.y + pcl.vy*vel_scale)))
    
    
    
    
    
    
    
    
    
    
    
