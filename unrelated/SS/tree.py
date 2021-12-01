from pcl import *

class Tree_root: #элемент дерева Square_tree
    def __init__ (root, parent, x, y, r):
        root.parent = parent  #родственные связи. Только у коренного элемента родитель None
        root.child_lu = None
        root.child_ru = None
        root.child_rd = None
        root.child_ld = None
        root.gas = set()         #множество частиц, перессекающихся с этим элементом. Все такие элементы полностью покрывают частицу.
        root.light = False       #наличие непустых gas в этом поддереве. 
        root.x = x  #координаты центра и полусторона
        root.y = y
        root.r = r
	
    def upd_light_up(root):
        light_was = False
        light_is = True
        while root is not None and (light_was != light_is):
            light_was = root.light
            root.light = (len(root.gas)!=0) or (root.child_lu is not None and root.child_lu.light) or (root.child_ru is not None and root.child_ru.light) or (root.child_rd is not None and root.child_rd.light) or (root.child_ld is not None and root.child_ld.light)
            light_is = root.light
            root = root.parent
        
    def make_lca_up(root, pcl):
        while pcl.x-root.x-pcl.r<-root.r or pcl.y-root.y-pcl.r<-root.r or pcl.x-root.x+pcl.r>root.r or pcl.y-root.y+pcl.r>root.r:
            if root.parent is None:
                if   pcl.x>root.x and pcl.y>root.y:
                    root.parent = Tree_root(None, root.x+root.r, root.y+root.r, root.r*2)
                    root.parent.child_lu = root
                elif pcl.x<root.x and pcl.y>root.y:
                    root.parent = Tree_root(None, root.x-root.r, root.y+root.r, root.r*2)
                    root.parent.child_ru = root
                elif pcl.x<root.x and pcl.y<root.y:
                    root.parent = Tree_root(None, root.x-root.r, root.y-root.r, root.r*2)
                    root.parent.child_rd = root
                else:
                    root.parent = Tree_root(None, root.x+root.r, root.y-root.r, root.r*2)
                    root.parent.child_ld = root
            root = root.parent
        return root
        
    def make_lca_down(root, pcl):
        while True:
            if   pcl.x-root.x<-pcl.r and pcl.y-root.y<-pcl.r:
                if root.child_lu is None:
                    root.child_lu = Tree_root(root, root.x-root.r/2, root.y-root.r/2, root.r/2)
                root = root.child_lu
            
            elif pcl.x-root.x>pcl.r and pcl.y-root.y<-pcl.r:
                if root.child_ru is None:
                    root.child_ru = Tree_root(root, root.x+root.r/2, root.y-root.r/2, root.r/2)
                root = root.child_ru
            
            elif pcl.x-root.x>pcl.r and pcl.y-root.y>pcl.r:
                if root.child_rd is None:
                    root.child_rd = Tree_root(root, root.x+root.r/2, root.y+root.r/2, root.r/2)
                root = root.child_rd
            
            elif pcl.x-root.x<-pcl.r and pcl.y-root.y>pcl.r:
                if root.child_ld is None:
                    root.child_ld = Tree_root(root, root.x-root.r/2, root.y+root.r/2, root.r/2)
                root = root.child_ld
            
            else:
                return root
    
    def make_cover(root, pcl, min_r, cover):
        if root.r<min_r*2:
            root.gas.add(pcl)
            cover.add(root)
        else:
            cover_lu = cover_ru = cover_rd = cover_ld = set()
            
            if pcl.x-root.x<pcl.r and pcl.y-root.y<pcl.r:
                if root.child_lu is None:
                    root.child_lu = Tree_root(root, root.x-root.r/2, root.y-root.r/2, root.r/2)
                cover_lu = root.child_lu.make_cover(pcl, min_r, cover)
            
            if pcl.x-root.x>-pcl.r and pcl.y-root.y<pcl.r:
                if root.child_ru is None:
                    root.child_ru = Tree_root(root, root.x+root.r/2, root.y-root.r/2, root.r/2)
                cover_ru = root.child_ru.make_cover(pcl, min_r, cover)
            
            if pcl.x-root.x>-pcl.r and pcl.y-root.y>-pcl.r:
                if root.child_rd is None:
                    root.child_rd = Tree_root(root, root.x+root.r/2, root.y+root.r/2, root.r/2)
                cover_rd = root.child_rd.make_cover(pcl, min_r, cover)
            
            if pcl.x-root.x<pcl.r and pcl.y-root.y>-pcl.r:
                if root.child_ld is None:
                    root.child_ld = Tree_root(root, root.x-root.r/2, root.y+root.r/2, root.r/2)
                cover_ld = root.child_ld.make_cover(pcl, min_r, cover)
    
    def get_intersect (root, intersect, gas_above):
        gas_this_and_above = gas_above | root.gas
        for pcl_1 in root.gas:
            for pcl_2 in gas_this_and_above:
                if pcl_1 is not pcl_2 and (pcl_1, pcl_2) not in intersect and (pcl_2, pcl_1) not in intersect:
                    intersect.add((pcl_1, pcl_2))
        if root.child_lu is not None and root.child_lu.light:
            root.child_lu.get_intersect(intersect, gas_this_and_above)
        if root.child_ru is not None and root.child_ru.light:
            root.child_ru.get_intersect(intersect, gas_this_and_above)
        if root.child_rd is not None and root.child_rd.light:
            root.child_rd.get_intersect(intersect, gas_this_and_above)
        if root.child_ld is not None and root.child_ld.light:
            root.child_ld.get_intersect(intersect, gas_this_and_above)
        del gas_this_and_above
    
    def draw_root (root, screen):
        pass
        
class Square_tree:
    def __init__ (tree, x=1, y=1, r=1):
        tree.lca = dict()
        tree.cover = dict()
        tree.root = Tree_root(None, x, y, r)
    
    def add_pcl(tree, pcl):
        tree.lca[pcl] = tree.root
        tree.cover[pcl] = set()
        tree.root.light = True
        tree.upd_pcl(pcl)
    
    def upd_pcl(tree, pcl):
        lca = tree.lca[pcl]
        lca = lca.make_lca_up(pcl)
        while tree.root.parent is not None:
            tree.root = tree.root.parent
        lca = lca.make_lca_down(pcl)
        tree.lca[pcl] = lca
        
        new_cover = set()
        lca.make_cover(pcl, pcl.r*1.0, new_cover)
        old_cover = tree.cover[pcl]
        
        for root in old_cover - new_cover:
            root.gas.remove(pcl)
            root.upd_light_up()
        
        for root in new_cover - old_cover:
            root.gas.add(pcl)
            root.upd_light_up()
        
        tree.cover[pcl] = new_cover
    
    def del_pcl(tree, pcl):
        for root in tree.cover[pcl]:
            root.gas.remove(gas)
            root.upd_light_up()
        
        del tree.lca[pcl]
        del tree.cover[pcl]
    
    def get_intersect(tree):
        intersect = set()
        gas_above = set()
        tree.root.get_intersect(intersect, gas_above)
        return intersect
    
