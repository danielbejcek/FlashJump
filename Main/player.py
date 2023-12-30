import pygame
import os
import sys
from Images.images import img_paths
from Main.player_animation import animate_character

class PlayerCharacter(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1792, 1024))
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.action = 'Idle'


        """Serves as a divider between actions. 0 is for idle, 1 is for running"""
        self.action_divider = 0

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # self.image = animate_character(self.action)[self.action_divider][self.frame_index]

        self.movement_y = [False, False]
        self.movement_x = [False, False]
        self.img_pos = [x, y]
        self.flip = False


    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.img_pos)

    def player_movement(self):
        """Y axis position"""
        self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 4

        """X axis position"""
        self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.action = 'Running'
                self.action_divider = 1
                self.frame_index = 0

                """Y axis"""
                # if event.key == pygame.K_w:
                #     self.movement_y[0] = True
                # if event.key == pygame.K_s:
                #     self.movement_y[1] = True
                """X axis"""
                if event.key == pygame.K_a:
                    self.movement_x[0] = True
                    self.flip = True
                    self.direction = -1

                if event.key == pygame.K_d:
                    self.movement_x[1] = True
                    self.flip = False
                    self.direction = 1

            if event.type == pygame.KEYUP:
                self.action = 'Idle'
                self.action_divider = 0
                self.frame_index = 0

                """Y axis"""
                # if event.key == pygame.K_w:
                #     self.movement_y[0] = False
                # if event.key == pygame.K_s:
                #     self.movement_y[1] = False
                """X axis"""
                if event.key == pygame.K_a:
                    self.movement_x[0] = False

                if event.key == pygame.K_d:
                    self.movement_x[1] = False

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        self.image = animate_character(self.action)[self.action_divider][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(animate_character(self.action)[self.action_divider]):
            self.frame_index = 0


