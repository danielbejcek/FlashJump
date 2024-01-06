import pygame
import os
from Images.images import img_paths

current_dir = os.path.dirname(__file__)
screen = pygame.display.set_mode((1792, 1024))
def animate_character(action):
    animation_list = []
    temp_list = []


    for i in os.listdir(os.path.join(current_dir,'..','Images','Characters','Player',action)):
        img = pygame.image.load(os.path.join(current_dir,'..','Images','Characters','Player',action,i))
        img = pygame.transform.scale(img, (int(img.get_width() // .8), (int(img.get_height() // .8))))

        if action == 'Idle':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Running':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Jump':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Bow':
            temp_list.append(img)
            animation_list.append(temp_list)

    return animation_list


def animate_arrow(flip,x_pos,y_pos):
    arrow_default = pygame.image.load(img_paths['arrow_default'])
    arrow_default = pygame.transform.scale(arrow_default, (int(arrow_default.get_width() * 1.3), (int(arrow_default.get_height() * 1.3))))
    screen.blit(pygame.transform.flip(arrow_default, flip, False), (x_pos, y_pos))
    # if flip == True:
    #     x_pos -= 10
    #     screen.blit(pygame.transform.flip(arrow_default, flip, False), (x_pos, y_pos))
    #
    # if flip == False:
    #     x_pos += 80
    #     screen.blit(pygame.transform.flip(arrow_default, flip, False), (x_pos, y_pos))


