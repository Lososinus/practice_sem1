class Motion_derivative:
    def __init__(k):
        k.x = dict()
        k.y = dict()
        k.vx = dict()
        k.vy = dict()

class Particle_6_12:
    def __init__(self, m=1, x=0, y=0, vx=0, vy=0, r=10, color=(0, 0, 0), disp_en=1, sigma=1, r_max=10):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.disp_en = disp_en
        self.sigma = sigma
        self.r_max = r_max
    
    def copy(self):
        return Particle_6_12 (m=self.m, x=self.x, y=self.y, vx=self.vx, vy=self.vy, r=self.r, color=self.color, disp_en=self.disp_en, sigma=self.sigma, r_max=self.r_max)
    
    @staticmethod
    def calc_coll(pcl_1, pcl_2):
    	#проверка на пересечение и сближение, обработка упругого столкновения 2 частиц.
        delta_x = pcl_2.x - pcl_1.x
        delta_y = pcl_2.y - pcl_1.y
        dist_sqr = delta_x**2 + delta_y**2
        if dist_sqr < (pcl_1.r + pcl_2.r)**2:
            dr_dot_dv = (pcl_2.vx-pcl_1.vx)*delta_x + (pcl_2.vy-pcl_1.vy)*delta_y
            if dr_dot_dv < 0:
                common_factor  = 2.0*dr_dot_dv/((pcl_1.m + pcl_2.m) * dist_sqr)
                pcl_1.vx += pcl_2.m * delta_x * common_factor
                pcl_1.vy += pcl_2.m * delta_y * common_factor
                pcl_2.vx -= pcl_1.m * delta_x * common_factor
                pcl_2.vy -= pcl_1.m * delta_y * common_factor
            return 1
        else:
            return 0
    
    @staticmethod
    def get_interaction_derivative(gas, intersect):
        k = Motion_derivative()
        for pcl in gas:
            k.x[pcl] = pcl.vx
            k.y[pcl] = pcl.vy
            k.vx[pcl] = 0
            k.vy[pcl] = 0
        
        for pair in intersect:
            pcl_1 = pair[0]
            pcl_2 = pair[1]
            delta_x = pcl_2.x - pcl_1.x
            delta_y = pcl_2.y - pcl_1.y
            dist_sqr = delta_x**2 + delta_y**2
            
            disp_en = (pcl_1.disp_en + pcl_2.disp_en) * 0.5
            sigma_sqr = ((pcl_1.sigma + pcl_2.sigma) * 0.5) ** 2
            forse_div_r = (24*disp_en/sigma_sqr) * (2*(sigma_sqr/dist_sqr)**7 - (sigma_sqr/dist_sqr)**4)
            k.vx[pcl_1] -= forse_div_r * delta_x
            k.vy[pcl_1] -= forse_div_r * delta_y
            k.vx[pcl_2] += forse_div_r * delta_x
            k.vy[pcl_2] += forse_div_r * delta_y
        
        for pcl in gas:
            k.vx[pcl] /= pcl.m
            k.vy[pcl] /= pcl.m
        return k
    
    @staticmethod
    def apply_derivative(gas, der, dt):
        for pcl in gas:
            pcl.x += dt * der.x[pcl]
            pcl.y += dt * der.y[pcl]
            pcl.vx += dt * der.vx[pcl]
            pcl.vy += dt * der.vy[pcl]
        
    @staticmethod
    def runge_kutta_6_12(gas, intersect, time_step):
        h = time_step  # в литературе шаг по времени обычно обозначают h
        
        k1 = Particle_6_12.get_interaction_derivative(gas, intersect)
        
        Particle_6_12.apply_derivative(gas, k1, h / 2)
        k2 = Particle_6_12.get_interaction_derivative(gas, intersect)
        Particle_6_12.apply_derivative(gas, k1, -h / 2)
        
        Particle_6_12.apply_derivative(gas, k2, h / 2)
        k3 = Particle_6_12.get_interaction_derivative(gas, intersect)
        Particle_6_12.apply_derivative(gas, k2, -h / 2)
        
        Particle_6_12.apply_derivative(gas, k3, h)
        k4 = Particle_6_12.get_interaction_derivative(gas, intersect)
        Particle_6_12.apply_derivative(gas, k3, -h)
        
        Particle_6_12.apply_derivative(gas, k1, h * 1 / 6)
        Particle_6_12.apply_derivative(gas, k2, h * 2 / 6)
        Particle_6_12.apply_derivative(gas, k3, h * 2 / 6)
        Particle_6_12.apply_derivative(gas, k4, h * 1 / 6)
    
    @staticmethod
    def calc_energy(gas, intersect):
        en = 0
        for pcl in gas:
            en += (pcl.vx**2 + pcl.vy**2)/2
        for pair in intersect:
            pcl_1 = pair[0]
            pcl_2 = pair[1]
            delta_x = pcl_2.x - pcl_1.x
            delta_y = pcl_2.y - pcl_1.y
            dist_sqr = delta_x**2 + delta_y**2
            
            disp_en = (pcl_1.disp_en + pcl_2.disp_en) * 0.5
            sigma_sqr = ((pcl_1.sigma + pcl_2.sigma) * 0.5) ** 2
            en += 4*disp_en * ((sigma_sqr/dist_sqr)**6 - (sigma_sqr/dist_sqr)**3)
        return en
