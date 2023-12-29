import pygame
import os

def animate_character(action):
    animation_list = []
    if action == 'Running':
        animation_list.clear()

    for i in os.listdir(f'../Images/Characters/Player/{action}'):
        img = pygame.image.load(f'../Images/Characters/Player/{action}/{i}')
        img = pygame.transform.scale(img, (int(img.get_width() // .7), (int(img.get_height() // .7))))
        animation_list.append(img)

    return animation_list

