from Main.player import PlayerCharacter
import pygame
from Main.player_animation import animate_enemy

class EnemyCharacter(PlayerCharacter):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.action = 'Idle'
        self.frame_index = 0
        self.flip = False
        self.movement_y = [False, True]
        self.movement_x = [False, False]
        self.img_pos = [x,y]






    def draw_enemy(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.img_pos)


    def update_enemy_animation(self):
        """
        self.image controls the image generator. We are accessing the list which is returned from animate_character function.
        We pass 'self.action_divider' that controls the nature of the action (idle, running etc...)
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced to prevent a 'list index out of range'.
        """

        self.image = animate_enemy(self.action)[self.action_divider][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > 80:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_enemy(self.action)[self.action_divider]):
            self.frame_index = 0