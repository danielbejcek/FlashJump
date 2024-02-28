import os
import pygame

current_dir = os.path.dirname(__file__)

"""pygame init to transform images"""
pygame.init()
screen = pygame.display.set_mode((1792, 1024))


img_paths = {
            "BG_image": os.path.join(current_dir, '..', 'Images', 'Background','main_bg.jpg'),
            "character_img": os.path.join(current_dir, '..', 'Images','Characters','character.png'),
            "char_idle": os.path.join(current_dir,'..','Images','Characters','Player','Idle','0.png'),
            "arrow_default": os.path.join(current_dir,'..', 'Images', 'Characters','Player','Arrow','Arrow.png'),
            "platform_0": os.path.join(current_dir,'..', 'Images', 'Platforms','platform_0.png'),
            "platform_1": os.path.join(current_dir,'..', 'Images', 'Platforms','platform_1.png')

        }

"""Main BG img"""
bg_img = pygame.image.load(img_paths['BG_image']).convert()

"""Main floor platform"""
platform_0 = pygame.image.load(img_paths['platform_0'])

platform_0.get_rect()

platform_1 = pygame.image.load(img_paths['platform_1'])

def draw_background():

    screen.blit(bg_img, (0, 0))
    screen.blit(platform_0,(0,900))
    screen.blit(platform_0,(835,900))
