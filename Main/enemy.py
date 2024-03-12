from Main.player import PlayerCharacter
import pygame
from Main.player_animation import animate_enemy
from Main.collisions import Collisions

class EnemyCharacter(PlayerCharacter):
    def __init__(self):
        super().__init__()
        # self.action = 'Idle'
        self.enemy_touchdown = False
        self.enemy_img_pos = [20,200]
        self.enemy_movement_y = [False, True]
        self.enemy_movement_x = [False, False]
        self.enemy_flip = False
        self.enemy_image = pygame.Surface((0,0))


    def draw_enemy(self):
        self.screen.blit(pygame.transform.flip(self.enemy_image, self.enemy_flip, False), self.enemy_img_pos)

    def update_enemy_hitbox(self,x,y):
        self.hitbox = (x + 70, y + 102,30,90)
        return self.hitbox

    def enemy_movement(self):
        """X axis position"""
        self.enemy_img_pos[0] += (self.enemy_movement_x[1] - self.enemy_movement_x[0]) * self.x_velocity

        """Y axis position"""
        self.enemy_img_pos[1] += (self.enemy_movement_y[1] - self.enemy_movement_y[0]) * self.y_velocity

    def update_enemy_animation(self):
        """
        self.image controls the image generator. We are accessing the list which is returned from animate_character function.
        We pass 'self.action_divider' that controls the nature of the action (idle, running etc...)
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced to prevent a 'list index out of range'.
        """

        self.enemy_image = animate_enemy(self.action)[self.action_divider][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > 80:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_enemy(self.action)[self.action_divider]):
            self.frame_index = 0

    # def add_enemy(self,hitbox,collision_object,character):
    #     self.draw_enemy()
    #     self.update_enemy_animation()
