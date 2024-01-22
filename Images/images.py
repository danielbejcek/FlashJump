import os
import pygame

current_dir = os.path.dirname(__file__)

"""pygame init to transform images"""
pygame.init()
screen = pygame.display.set_mode((1792, 1024))


img_paths = {
            "BG_image": os.path.join(current_dir, '..', 'Images', 'BG_MAIN.png'),
            "character_img": os.path.join(current_dir, '..', 'Images','Characters','character.png'),
            "char_idle": os.path.join(current_dir,'..','Images','Characters','Player','Idle','0.png'),
            "leaf_particle_1": os.path.join(current_dir,'..', 'Images', 'Particles', 'leaf_particle_1.png'),
            "arrow_default": os.path.join(current_dir,'..', 'Images', 'Characters','Player','Arrow','Arrow.png')

        }

bg_img = pygame.image.load(img_paths['BG_image']).convert()
