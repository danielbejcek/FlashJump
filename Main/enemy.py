from Main.player import PlayerCharacter
import pygame
from Main.player_animation import animate_enemy
from Main.collisions import Collisions

class EnemyCharacter(PlayerCharacter):
    def __init__(self):
        super().__init__()
        self.enemy_action, self.enemy_action_divider = 'Idle', 0

        """Enemy attack variables"""
        self.enemy_attack = False
        self.enemy_attack_start_time = None
        self.enemy_attack_duration = 500

        self.enemy_touchdown = False
        self.enemy_img_pos = [200,600]
        self.enemy_movement_y = [False, True]
        self.enemy_movement_x = [False, False]
        self.enemy_x_velocity = 3
        self.enemy_flip = False
        self.enemy_image = pygame.Surface((0,0))
        self.enemy_hitpoints = 100

        self.enemy_list = []
        self.enemy_spawn_rate = 2000
        self.enemy_current_spawn = pygame.time.get_ticks()


    def draw_enemy(self):
        self.screen.blit(pygame.transform.flip(self.enemy_image, self.enemy_flip, False), self.enemy_img_pos)

    def update_enemy_hitbox(self,x,y):
        self.hitbox = (x + 80, y + 102,30,90)
        return self.hitbox

    def enemy_movement(self,player_pos,enemy_attack):
        self.enemy_horizontal_range = [player_pos[0] - 90, player_pos[0] + 70]

        enemy_attack = self.enemy_attack
        """X axis position"""
        # if not self.enemy_attack:
        self.enemy_img_pos[0] += (self.enemy_movement_x[1] - self.enemy_movement_x[0]) * self.enemy_x_velocity
        self.enemy_action, self.action_divider = "Running", 1

        """Enemy left side of the player movement"""
        if self.enemy_img_pos[0] <= self.enemy_horizontal_range[0]:
            self.enemy_flip = False
            self.enemy_movement_x[1] = True

        """Condition that checks if the enemy is within the 'LEFT' side range of the player"""
        if self.enemy_img_pos[0] > self.enemy_horizontal_range[0] and self.enemy_img_pos[0] <= player_pos[0]:
            self.enemy_movement_x[1] = False
            self.enemy_action, self.action_divider = "Idle", 0

            """Condition that checks if the player's vertical axis matches the one of the enemy"""
            if player_pos[1] >= self.enemy_img_pos[1]:
                print("LEFT")


        """Enemy right side of the player movement"""
        if self.enemy_img_pos[0] >= self.enemy_horizontal_range[1]:
            self.enemy_flip = True
            self.enemy_movement_x[0] = True

        """Condition that checks if the enemy is within the 'RIGHT' side range of the player"""
        if self.enemy_img_pos[0] < self.enemy_horizontal_range[1] and self.enemy_img_pos[0] >= player_pos[0]:
            self.enemy_movement_x[0] = False
            self.enemy_action, self.action_divider = "Idle", 0

            """Condition that checks if the player's vertical axis matches the one of the enemy"""
            if player_pos[1] >= self.enemy_img_pos[1]:
                print("RIGHT")


        """Y axis position"""
        self.enemy_img_pos[1] += (self.enemy_movement_y[1] - self.enemy_movement_y[0]) * self.y_velocity

    def update_enemy_animation(self):
        """
        self.image controls the image generator. We are accessing the list which is returned from animate_enemy function.
        We pass 'self.action_divider' that controls the nature of the action (idle, running etc...)
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced to prevent a 'list index out of range'.
        """
        self.enemy_image = animate_enemy(self.enemy_action)[self.enemy_action_divider][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > 80:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_enemy(self.enemy_action)[self.enemy_action_divider]):
            self.frame_index = 0

        if self.enemy_attack:
            self.enemy_action, self.enemy_action_divider = "Attack", 2
            self.enemy_image = animate_enemy(self.enemy_action)[self.enemy_action_divider][self.frame_index]
            self.enemy_movement_x = [False,False]
            if pygame.time.get_ticks() - self.enemy_attack_start_time > self.enemy_attack_duration:
                self.enemy_attack = False
                self.enemy_attack_start_time = None

    """
    Method for adding enemies in a time oriented order. We pass 'enemy_object' and 'current_time' from main game loop as arguments.
    Each time the 'current_time' surpasses the 'self.enemy_spawn_rate', 'enemy_object' is added to the list
    and 'self.enemy_current_spawn' is updated with current time to maintain correct order and continuous flow of adding 'enemy_object'.
    """
    def add_enemy(self, enemy_object, current_time):
        if current_time - self.enemy_current_spawn > self.enemy_spawn_rate:
            self.enemy_list.append(enemy_object)
            self.enemy_current_spawn = current_time
        return self.enemy_list