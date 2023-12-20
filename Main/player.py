import pygame
import os
from Images.images import img_paths

class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)

        self.movement_y = [False, False]
        self.movement_x = [False, False]
        self.img_pos = [x, y]
        self.img = pygame.image.load(img_paths["character_img"])
        self.character_img = pygame.transform.scale(self.img, (int(self.img.get_width() // 2), (int(self.img.get_height() // 2))))

