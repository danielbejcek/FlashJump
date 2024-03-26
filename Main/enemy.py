from Main.player import PlayerCharacter
import pygame
from Main.player_animation import animate_enemy
from Main.collisions import Collisions

class EnemyCharacter(PlayerCharacter):
    def __init__(self):
        super().__init__()
        self.enemy_action, self.enemy_action_divider = 'Idle', 0
        self.enemy_image = pygame.Surface((0, 0))

        """Enemy attack variables"""
        self.enemy_attack = False
        self.enemy_attack_start_time = None
        self.enemy_attack_duration = 500
        self.enemy_attack_window = False

        """Enemy movement variable"""
        self.enemy_touchdown = False
        self.enemy_img_pos = [50,600]
        self.enemy_movement_y = [False, True]
        self.enemy_movement_x = [False, False]
        self.enemy_x_velocity = 3
        self.enemy_flip = False

        """Enemy attributes"""
        self.enemy_hitpoints = 100

        """Multiple enemies configuration"""
        self.enemy_list = []
        self.enemy_spawn_rate = 2000
        self.enemy_current_spawn = pygame.time.get_ticks()
        self.enemy_collide = False


    def draw_enemy(self):
        self.screen.blit(pygame.transform.flip(self.enemy_image, self.enemy_flip, False), self.enemy_img_pos)

    def update_enemy_hitbox(self,x,y):
        self.hitbox = (x + 80, y + 102,30,90)
        return self.hitbox


    def enemy_movement(self,player_pos):
        """Setting up an attack window for the enemy character that constantly checks if player is within enemy's attack range"""
        self.enemy_attack_window = False

        """Range of player's hitbox that allows the enemies to attack once within this range"""
        self.enemy_horizontal_range = [player_pos[0] - 90, player_pos[0] + 70]


        """X axis position"""
        self.enemy_img_pos[0] += (self.enemy_movement_x[1] - self.enemy_movement_x[0]) * self.enemy_x_velocity
        if self.enemy_movement_x[0] or self.enemy_movement_x[1]:
            self.enemy_action, self.action_divider = "Running", 1
        else:
            self.enemy_action, self.action_divider = "Idle", 0


        """If enemy is not within the player's left 'horizontal_range', start to move towards him"""
        if self.enemy_img_pos[0] <= self.enemy_horizontal_range[0]:
            self.enemy_flip = False
            self.enemy_movement_x[1] = True

        """Condition that checks if the enemy is within the left 'horizontal_range' of the player"""
        if self.enemy_img_pos[0] > self.enemy_horizontal_range[0] and self.enemy_img_pos[0] <= player_pos[0]:
            self.enemy_movement_x[1] = False


            """
            Condition that checks if the player's vertical axis matches the one of the enemy.
            Once these conditions are met, enemy is set up for an attack sequence
            """
            if player_pos[1] >= self.enemy_img_pos[1]:
                self.enemy_attack_window = True
        #         Placeholder for enemy attack animation


        """If enemy is not within the player's right 'horizontal range', start to move towards him"""
        if self.enemy_img_pos[0] >= self.enemy_horizontal_range[1]:
            self.enemy_flip = True
            self.enemy_movement_x[0] = True

        """Condition that checks if the enemy is within the right 'horizontal range' of the player"""
        if self.enemy_img_pos[0] < self.enemy_horizontal_range[1] and self.enemy_img_pos[0] >= player_pos[0]:
            self.enemy_movement_x[0] = False

            """
            Condition that checks if the player's vertical axis matches the one of the enemy.
            Once these conditions are met, enemy is set up for an attack sequence.
            """
            if player_pos[1] >= self.enemy_img_pos[1]:
                self.enemy_attack_window = True
        #     Placeholder for enemy attack animation


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
    Each time the 'current_time' value surpasses the value of 'self.enemy_spawn_rate', 'enemy_object' is added to the list
    and 'self.enemy_current_spawn' is updated with current time to maintain correct order and continuous flow of adding 'enemy_object'.
    """
    def add_enemy(self,current_time):
        self.enemy = EnemyCharacter()
        if self.enemy_list == []:
            self.enemy_list.append(self.enemy)

        if current_time - self.enemy_current_spawn > self.enemy_spawn_rate:
            if len(self.enemy_list) <= 0:
                self.enemy_list.append(self.enemy)
                self.enemy_current_spawn = current_time

        return self.enemy_list



    def hit_register(self,character,melee_attack_register,type):
        character.enemy_hitpoints = self.enemy_hitpoints
        if type == "enemy":
            if character.enemy_attack_window and melee_attack_register:
                character.enemy_hitpoints -= 50

        print(character.enemy_hitpoints)
