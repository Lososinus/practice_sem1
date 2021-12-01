import pygame as pg

class Particle:
    pg.init()
    def __init__(self, m=1, r=10, color=(0, 0, 0), x=0, y=0, vx=0, vy=0):
        self.m = m
        self.r = r
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def coll_pcl(pcl_1, pcl_2):
    	#Расчёт скоростей после упругого столкновени 2 частиц. Включает проверку на пересечение.
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

    def move_dt(self, dt, g):
        # обрабатывает итерацию движения частицы за dt
        self.x+= self.vx*dt
        self.y+= self.vy*dt - 0.5*g*dt**2
        self.vy-= g*dt

    def draw_pcl(self, surf):
    	#рисует частицу на поверхности surf
        pg.draw.circle (surf, self.color, (round(self.x), round(self.y)), round(self.r))
        pg.draw.circle (surf, (200, 200, 200), (round(self.x), round(self.y)), round(self.r), 1)
