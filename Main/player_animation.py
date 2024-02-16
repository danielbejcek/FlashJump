import pygame
import os

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

        if action == 'Attack_1':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Attack_2':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Landing':
            temp_list.append(img)
            animation_list.append(temp_list)


    return animation_list












































