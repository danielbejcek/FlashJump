import pygame
import os
import sys
from Images.images import img_paths
from Main.player_animation import animate_character
from Main.Collisions import draw_floor


class PlayerCharacter(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1792, 1024))
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.action = 'Idle'

        """Serves as a divider between actions. 0 is for idle, 1 is for running"""
        self.action_divider = 0

        """'self.frame_index' serves to access the specific image as an index in a 'animation_list' received from 'animate_character' function."""
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.jump = False
        self.jump_velocity = -15
        self.movement_y = [False, False]
        self.movement_x = [False, False]
        self.img_pos = [x, y]
        self.flip = False

        """
        Variables that help control the movement of the character. When user presses 'Key_A' to run left and right after 'Key_D' to run right,
        character will stop and enter 'Idle' animation, until one of the keys is released.
        """
        self.motion_left = False
        self.motion_right = False

    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.img_pos)

    def player_movement(self):
        """Y axis position"""
        self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 1

        """X axis position"""
        self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * 4
        # self.movement_y[1] = True
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self.action = 'Running'
                self.action_divider = 1
                self.frame_index = 0

                """X axis"""
                if event.key == pygame.K_a:
                    self.movement_x[0] = True
                    self.flip = True
                    self.motion_left = True

                if event.key == pygame.K_d:
                    self.movement_x[1] = True
                    self.flip = False
                    self.motion_right = True

                if event.key == pygame.K_SPACE:
                    self.action = 'Jump'
                    # self.movement_y[1] = False
                    # self.movement_y[0] = True



                if self.motion_right and self.motion_left:
                    self.action = 'Idle'


            if event.type == pygame.KEYUP:
                self.action = 'Idle'
                self.action_divider = 0
                self.frame_index = 0

                """X axis"""
                if event.key == pygame.K_a:
                    self.motion_left = False
                    self.movement_x[0] = False
                    if self.motion_right:
                        self.flip = False
                        self.action = 'Running'

                if event.key == pygame.K_d:
                    self.motion_right = False
                    self.movement_x[1] = False
                    if self.motion_left:
                        self.flip = True
                        self.action = 'Running'

                if event.key == pygame.K_SPACE:
                    # self.action = 'Jump'
                    self.jump = False
                    self.movement_y[0] = False
                    # self.movement_y[1] = True



    def update_animation(self):
        ANIMATION_COOLDOWN = 80

        """
        self.image controls the image generator. We are accessing the list which is returned from animate_character function.
        We pass 'self.action_divider' that controls the nature of the action (either idle or running) 
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced.
        """
        self.image = animate_character(self.action)[self.action_divider][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_character(self.action)[self.action_divider]):
            self.frame_index = 0


