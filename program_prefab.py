


import pygame
import random
import os
import tkinter
from funciones_de_calculo import *





"""ancho y alto"""
scale_screen = [1280,720]
#scale_screen = [tkinter.Tk().winfo_screenwidth(),tkinter.Tk().winfo_screenheight()]

"""iniciar pantalla"""

pygame.init()



screen = pygame.display.set_mode(scale_screen, pygame.RESIZABLE)
pygame.display.set_caption('')

pygame.display.set_icon(pygame.Surface((32,32)))









def return_spritesheet(img,rect,cantidad_frame,hori_vert_bool,list_bool_flip,scale):
    listi = []
    
    num = 0
    for i in range(1,cantidad_frame+1):
        #print(rect)
        listi.append(pygame.transform.flip(pygame.transform.scale(pygame.Surface.subsurface(img,(rect[0],rect[1]),(rect[2],rect[3])),(rect[2]*scale,rect[3]*scale)),list_bool_flip[0],list_bool_flip[1]))
        if hori_vert_bool[0] == True:
            rect[0] += rect[2]
        if hori_vert_bool[1] == True:
            rect[1] += rect[3]
    return listi
def create_sprite_list(img,scale=3,num=0,frames_total=5,total_directions=8,hort_vert_bool=[True,False],hort_vert_bool_rotate=[[False,False],[False,False],[True,False],[False,False],[False,False],[False,False],[True,False],[False,False]],rects=[[1,66,17,32],[18,0,17,32],[18,33,17,32],[18,33,17,32],[572,66,21,34],[597,0,22,34],[725,33,29,34],[725,33,29,34]]):
    listi = []
    #num = 0
    for i in range(1,total_directions+1):
        print(rects[num],num)
        
        listi.append(return_spritesheet(img,rects[num],frames_total,hort_vert_bool,hort_vert_bool_rotate[num],scale))
        num += 1
    return listi








class player:
    """fps"""
    fps = 60
    bool_game = True
    """directory"""
    dir = os.getcwd()+'/'
    """minimap"""
    minimap = None
    """menu"""
    menu = None
    """function extras"""
    function_normal = None
    function_in_menu = None
    function_keyboard = None
    
    def __init__(self, screen):
        """asignar"""
        self.screen = screen
        """utilizar"""
        while self.bool_game == True:

            pygame.time.Clock().tick(self.fps)
            """func"""
            if self.function_normal is not None:
                self.function_normal()

            """mostrar"""
            if self.menu is not None:
                self.menu(self.screen)
                if self.function_in_menu is not None:
                    self.function_in_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.bool_game = False      
                
            pygame.display.flip()
        
            


    


class Menu:
    image_background = None
    palabra = {'txt':'dbz legacy of battle','pos':(0,680),'scale':42,'color':(255,255,255)}
    """activar o desactivar menu"""
    active = True
    """especial"""
    version = {'txt':'1.0.0','pos':(0,500),'scale':32,'color':(255,0,0)}
    def __init__(self,screen):
        self.screen = screen
        if self.active == True:
            if self.image_background is not None:
                self.screen.blit(self.image_background,(0,0))
            string_blit(self.version['txt'],self.version['pos'],self.version['scale'],self.version['color'],screen)
            string_blit(self.palabra['txt'],self.palabra['pos'],self.palabra['scale'],self.palabra['color'],screen)
    
"""menu"""
menu = Menu




"""functs"""
def IF(valor,igual,retorno=True,retorno_else=False):
    if valor == igual:
        return retorno
    else:
        return retorno_else



def index_for_angle(dict_ind,pos_cursor):
    angul = round(angle(dict_ind['rect_list'][0],pos_cursor))
    list_anguls = [90,-90,180,0]
    dict_ind['indice'][0] = indice_numero_mas_cercano(list_anguls,angul)
    
    
def create_the_npcs(list_imgs,id_map,cantidad=1,area_pos=[0,0],area_dimention=[0,0],vel_tran=0.15,vel_move=5,dimention_surf=[32,32],max_num_lag=30,life=300,max_life=300,max_num_change=3):
    npcs = {'id_map':id_map,'cantidad':cantidad,'list_img': list_imgs,'rect_list':[],'center_rect':[(0,0)],'vel_transition':vel_tran,'vel_move':vel_move,'life_list':life,'max_life':max_life,'vel_recovery':1,'indice':[],'number_change':[],'max_num_change':max_num_change,'scale':dimention_surf,'num_lag':0,'max_num_lag':max_num_lag,'sum_index':0,'multiply_index':1,'all_elements_img':len(list_imgs)}
    indice_obtencion = 0
    num_pa_verificar = 0
    for i in range(1,cantidad+1):
        num_pa_verificar += 1
        npcs['center_rect'].append((random.randint(area_pos[0],area_pos[0]+area_dimention[0]),random.randint(area_pos[1],area_pos[1]+area_dimention[1])))

    if num_pa_verificar > 0:
        for i in range(1, cantidad + 1):
            npcs['indice'].append(0)
            npcs['number_change'].append(0)
            indice_obtencion += 1
            npcs['rect_list'].append(pygame.Rect(npcs['center_rect'][indice_obtencion],npcs['scale']))
    return npcs
def Avatar(screen,npc_dict,punch_bool=False):
    indice = 0
    #npc_dict['all_elements_img'],
    if npc_dict['indice'][indice]+ npc_dict['sum_index'] < len(npc_dict['list_img']):
        screen.blit(npc_dict['list_img'][npc_dict['indice'][indice]+ npc_dict['sum_index']][round(npc_dict['number_change'][indice])], npc_dict['rect_list'][indice])
        npc_dict['number_change'][indice] = clock(npc_dict['number_change'][indice],npc_dict['max_num_change'],npc_dict['vel_transition'])
    """arriba y abajo"""
    pos_mouse = pygame.mouse.get_pos()
    npc_dict['rect_list'][indice][0] = num_follow(npc_dict['rect_list'][indice][0],pos_mouse[0], npc_dict['vel_move'])
    npc_dict['rect_list'][indice][1] = num_follow(npc_dict['rect_list'][indice][1],pos_mouse[1], npc_dict['vel_move'])
    """mover multiplicador"""
    npc_dict['sum_index'] = IF(punch_bool,True,4,0)
        

    
        

def Colliderect(rect,rect2):
    hit = Hit_box(rect,rect2,0)
    if hit[0] == True or hit[1] == True or hit[2] == True or hit[3] == True:
        return True
    else:
        return False



        
    
def move_npc_for_enemy(screen,npc_dict,npc_dict_2):
    indice = indice_punto_mas_cercano(npc_dict_2['rect_list'][0],npc_dict['rect_list'])
    if npc_dict['indice'][indice]+ npc_dict['sum_index'] < npc_dict['all_elements_img']:
        screen.blit(npc_dict['list_img'][npc_dict['indice'][indice]+npc_dict['sum_index']][round(npc_dict['number_change'][0])],npc_dict['rect_list'][0])#
            
    colision = Colliderect(npc_dict['rect_list'][indice],npc_dict_2['rect_list'][indice]) 
        
    npc_dict['sum_index'] = IF(colision,True,0,0)

            
    index_for_angle(npc_dict,npc_dict_2['rect_list'][0])
    
    npc_dict['number_change'][indice] = clock(npc_dict['number_change'][indice],npc_dict['max_num_change'],npc_dict['vel_transition'])
    """arriba y abajo"""
    npc_dict['rect_list'][indice][0] = num_follow(npc_dict['rect_list'][indice][0],npc_dict_2['rect_list'][0][0], npc_dict['vel_move'])
    npc_dict['rect_list'][indice][1] = num_follow(npc_dict['rect_list'][indice][1],npc_dict_2['rect_list'][0][1], npc_dict['vel_move'])
         
        

                
            




"""definir algo"""

















"""math funcs"""
def Collide(fighter,enemy,vel,distance,box_map,bool_reject,impulso):
    hit_box = Hit_box([fighter['rect_list'][0][0],fighter['rect_list'][0][1],fighter['scale'][0],fighter['scale'][1]], 
                      [enemy['rect_list'][0][0],enemy['rect_list'][0][1],enemy['scale'][0],enemy['scale'][1]],distance)
    #hit_box_of_enem = Hit_box([pos_p2.x,pos_p2.y,32,32],[pos_p1.x,pos_p1.y,32,32],0)
    #no col player
    if bool_reject == False:
        if hit_box[0] == True:
            fighter['rect_list'][0][1] = num_follow(fighter['rect_list'][0][1],box_map[1]+box_map[3],vel)
        if hit_box[1] == True:
            fighter['rect_list'][0][1] = num_follow(fighter['rect_list'][0][1],box_map[1],vel)
        if hit_box[2] == True:
            fighter['rect_list'][0][0] = num_follow(fighter['rect_list'][0][0],box_map[0]+box_map[2],vel)
        if hit_box[3] == True:
            fighter['rect_list'][0][0] = num_follow(fighter['rect_list'][0][0],box_map[0],vel)
    #col player
    if bool_reject == True:
        if hit_box[1] == True:
            enemy['rect_list'][0][1] = num_follow(enemy['rect_list'][0][1],box_map[1]+box_map[3],impulso)
        if hit_box[0] == True:
            enemy['rect_list'][0][1] = num_follow(enemy['rect_list'][0][1],box_map[1],impulso)
        if hit_box[3] == True:
            enemy['rect_list'][0][0] = num_follow(enemy['rect_list'][0][0],box_map[0]+box_map[2],impulso)
        if hit_box[2] == True:
            enemy['rect_list'][0][0] = num_follow(enemy['rect_list'][0][0],box_map[0],impulso)

"""text func"""
def string_blit(text,pos,scale,color,screen):
    fuente_uni = pygame.font.Font(None, scale)
    mensaje_uni = fuente_uni.render(text, True, color)
    screen.blit(mensaje_uni, pos)





"""button funcs"""
#main
#create
def create_button(screen,dict,bool_active):
    button = pygame.Surface(dict['escala'])
    
    
    if Hover(pygame.mouse.get_pos(),[dict['pos'][0],dict['pos'][1],dict['escala'][0],dict['escala'][1]]) == False:
        button.fill(dict['color'])
        screen.blit(button,dict['pos'])
    if Hover(pygame.mouse.get_pos(),[dict['pos'][0],dict['pos'][1],dict['escala'][0],dict['escala'][1]]) == True:
        button.fill(dict['color_hover'])
        screen.blit(button,dict['pos'])
        if bool_active == True:
            dict['funcion']()
    string_blit(dict['string'],dict['pos'],dict['string_scale'],dict['string_color'],screen)

    










