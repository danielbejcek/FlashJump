import pygame


class Collisions:
    screen = pygame.display.set_mode((1792, 1024))
    def __init__(self):
        pass

    def platform_collision(self):
        platform_list = []
        floor = pygame.Rect(0, 900, 1792, 2)
        lamp = pygame.Rect(1002, 748, 185, 2)
        right_roof = pygame.Rect(1348, 626, 200, 2)
        chimney = pygame.Rect(1660, 464, 100, 2)
        second_right_roof = pygame.Rect(1375, 351, 150, 2)
        tent = pygame.Rect(511, 756, 290, 2)
        sky_platform_right = pygame.Rect(958, 281, 175, 2)
        sky_platform_left = pygame.Rect(555, 281, 175, 2)
        sky_platform_bottom = pygame.Rect(555, 452, 175, 2)
        left_roof = pygame.Rect(145, 622, 290, 2)

        platform_list.append(floor)
        platform_list.append(lamp)
        platform_list.append(right_roof)
        platform_list.append(chimney)
        platform_list.append(second_right_roof)
        platform_list.append(tent)
        platform_list.append(sky_platform_right)
        platform_list.append(sky_platform_left)
        platform_list.append(sky_platform_bottom)
        platform_list.append(left_roof)

        return platform_list

    """
    Method that checks for character's vertical position. 
    Whenever the player is touching the ground, 'self.touchdown' is set to True.
    Whenever player proceeds to press the SPACE button, 'self.touchdown' is set to False.
    The main movement of the character's apparatus is changing according to this variable.
    """
    def check_vertical_collision(self,hitbox, character,type):

        """
        self.touchdown is set to False at the beginning of the method.
        If a collision is detected, it is set to True. If no collision occurs, it remains False.
        Method is being updated in every frame of the loop to ensure proper collision functionality.
        """

        platforms = self.platform_collision()
        character.touchdown = False

        for platform in platforms:
            # pygame.draw.rect(self.screen, (255, 0, 0,), platform)

            """
            Once collision hitbox is met with one of the platform objects, 
            vertical variables are set accordingly for the player to be able to use the platform.
            """
            if type == "enemy":
                if hitbox.colliderect(platform):
                    character.enemy_touchdown = True
                    character.enemy_movement_y[1] = False
                    character.enemy_img_pos[1] = platform.top - character.enemy_image.get_height()
                    # pygame.draw.rect(self.screen, (100, 100, 100,), platform)

            if type == "player":
                if hitbox.colliderect(platform) and character.descent == False:

                    if character.jump == False:
                        character.y_velocity = 8
                        character.movement_y[1] = False
                        character.img_pos[1] = platform.top - character.image.get_height()
                        character.peak = False
                        character.touchdown = True
                        character.action, character.action_divider = 'Idle', 0
                        # pygame.draw.rect(self.screen, (100, 100, 100,), platform)


            """
            Whenever player wants to descent and presses the 'S' key, current platform is stored in 'self.drop_platform' variable, 
            usable only when colliding with platform -> 'self.touchdown == True'.
            If player is on floor platform, condition will not be triggered.
            """
            if pygame.key.get_pressed()[pygame.K_s] and character.touchdown == True:
                if platform == platforms[0]:
                    character.descent = False
                else:
                    character.drop_platform = platform
                    character.descent = True

            """
            Once 'self.descent' is set to True, player will disengage from the current platform and drop one level lower.
            Once the player's hitbox is no longer within the collision range of 'self.drop_platform', 'self.descent' is again set to False
            to allow regular collision with platforms bellow.
            """
            if character.descent == True:
                if hitbox.colliderect(character.drop_platform):
                    character.touchdown = False
                    character.movement_y[1] = True
                else:
                    character.descent = False
                    character.movement_y[1] = False
                    character.touchdown = True

        """
        If jump animation is not detected, character will now perform a 'Landing' animation,
        as he is falling from the edge of the collision platform towards the ground.
        """
        if not character.touchdown:
            if not character.jump:
                character.movement_y[1] = True
                character.peak = True
                character.action, character.action_divider = 'Landing', 6

    """
    Method that checks for horizontal hitbox collision between the enemy objects.
    Once enemies collide between themselves a small gap will be implemented to prevent image overlapping.
    """
    def check_horizontal_collision(self,enemy_object_list):

        for i in range(len(enemy_object_list)):
            for j in range(i + 1, len(enemy_object_list)):

                enemy1 = enemy_object_list[i]
                enemy2 = enemy_object_list[j]

                hitbox1 = pygame.Rect(enemy1.update_enemy_hitbox(enemy1.enemy_img_pos[0], enemy1.enemy_img_pos[1]))
                hitbox2 = pygame.Rect(enemy2.update_enemy_hitbox(enemy2.enemy_img_pos[0], enemy2.enemy_img_pos[1]))
                pygame.draw.rect(self.screen, (255, 0, 0), hitbox1, 1)
                pygame.draw.rect(self.screen, (0, 0, 0), hitbox2, 1)

                if hitbox2.colliderect(hitbox1):

                    enemy2.enemy_movement_x = [False,False]



    def hit_register(self,player_type,attack_type):
        pass
