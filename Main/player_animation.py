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

        # 0
        if action == 'Idle':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 1
        if action == 'Running':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 2
        if action == 'Jump':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 3
        if action == 'Bow':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 4
        if action == 'Attack_1':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 5
        if action == 'Attack_2':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 6
        if action == 'Landing':
            temp_list.append(img)
            animation_list.append(temp_list)


    return animation_list


def animate_enemy(action):
    animation_list = []
    temp_list = []

    for i in os.listdir(os.path.join(current_dir,'..','Images','Characters','Enemy',action)):
        img = pygame.image.load(os.path.join(current_dir,'..','Images','Characters','Enemy',action,i))
        img = pygame.transform.scale(img, (int(img.get_width() * 1.5), (int(img.get_height() * 1.5))))

        # 0
        if action == 'Idle':
            temp_list.append(img)
            animation_list.append(temp_list)
        # 1
        if action == "Running":
            temp_list.append(img)
            animation_list.append(temp_list)
        # 2
        if action == 'Attack':
            temp_list.append(img)
            animation_list.append(temp_list)

    return animation_list







































