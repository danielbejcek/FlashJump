import pygame
import sys
from Images import images
from Main.player_animation import animate_character, animate_arrow


class PlayerCharacter(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1792, 1024))
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        """Character is starting in an 'Idle' animation"""
        self.action = 'Idle'

        """Serves as a divider between actions. 0 is for idle, 1 is for running etc..."""
        self.action_divider = 0

        """'self.frame_index' serves to access the specific image as an index in a 'animation_list' received from 'animate_character' function."""
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        """Main movement variables"""
        self.movement_y = [False, True]
        self.movement_x = [False, False]
        self.img_pos = [x, y]
        self.flip = False

        """Jump animation variables"""
        self.jump = False
        self.jump_start_time = None
        self.jump_duration = 800

        """Bow animation variables"""
        self.bow = False
        self.bow_start_time = None
        self.bow_duration = 600

        """Arrow object variables"""
        self.arrow = False
        self.arrow_y = self.img_pos[1] + 53
        self.arrow_x = None
        self.arrow_direction = None

        """Collision floor temporary var"""
        self.floor_test = 770

        """
        Variables that help control the movement of the character. When user presses 'Key_A' to run left and right after 'Key_D' to run right,
        character will stop and enter 'Idle' animation, until one of the keys is released.
        """
        self.motion_left = False
        self.motion_right = False

    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.img_pos)

    def player_movement(self):
        """X axis position"""
        self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * 4

        """Y axis position"""
        self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 4

        """Help conditions to manipulate character more precisely after touching the ground"""
        if self.img_pos[1] >= self.floor_test:
            self.jump = False
            self.img_pos[1] = self.floor_test

            if not any(pygame.key.get_pressed()):
                self.action, self.action_divider = 'Idle', 0

            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                self.action, self.action_divider = 'Running', 1


            if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]:
                self.action, self.action_divider = 'Idle', 0



        """Main player movement loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if self.jump == False:
                if event.type == pygame.KEYDOWN and self.bow == False:
                    self.action, self.action_divider = 'Running', 1

                    """X axis"""
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                        self.flip = True
                        self.motion_left = True

                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                        self.flip = False
                        self.motion_right = True

                    """Y axis"""
                    if event.key == pygame.K_SPACE:
                        self.jump = True
                        self.jump_start_time = pygame.time.get_ticks()

                    """Bow animation"""
                    if event.key == pygame.K_e:
                        self.bow = True
                        self.arrow = True
                        self.frame_index = 0
                        self.bow_start_time = pygame.time.get_ticks()

                        """Arrow object orientation"""
                        self.arrow_direction = self.flip
                        if self.flip:
                            self.arrow_x = self.img_pos[0]
                        if not self.flip:
                            self.arrow_x = self.img_pos[0]



                if event.type == pygame.KEYUP:
                    self.action, self.action_divider = 'Idle', 0

                    """X axis"""
                    if event.key == pygame.K_a:
                        self.motion_left = False
                        self.movement_x[0] = False
                        if self.motion_right:
                            self.flip = False

                    if event.key == pygame.K_d:
                        self.motion_right = False
                        self.movement_x[1] = False
                        if self.motion_left:
                            self.flip = True

            """Jump action movement control"""
            if self.jump == True and self.bow == False:
                if event.type == pygame.KEYDOWN:
                    self.action, self.action_divider = 'Jump', 2

                    """X axis"""
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                        self.flip = True
                        self.motion_left = True

                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                        self.flip = False
                        self.motion_right = True

                if event.type == pygame.KEYUP:
                    """X axis"""
                    if event.key == pygame.K_a:
                        self.motion_left = False
                        self.movement_x[0] = False
                        if self.motion_right:
                            self.flip = False

                    if event.key == pygame.K_d:
                        self.motion_right = False
                        self.movement_x[1] = False
                        if self.motion_left:
                            self.flip = True


    def update_animation(self):
        """
        self.image controls the image generator. We are accessing the list which is returned from animate_character function.
        We pass 'self.action_divider' that controls the nature of the action (idle, running etc...) 
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced.
        """
        self.image = animate_character(self.action)[self.action_divider][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > 80:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_character(self.action)[self.action_divider]):
            self.frame_index = 0

        if self.jump_start_time is not None:
            current_jump_time = pygame.time.get_ticks()
            """Increase Y axis while jump is active"""
            self.movement_y[1] = False
            self.movement_y[0] = True

            if current_jump_time - self.jump_start_time > self.jump_duration:
                """Once jump animation is finished, apply gravity with 'self.movement[1] = True' again"""
                self.movement_y[0] = False
                self.movement_y[1] = True
                self.jump_start_time = None

        """Bow animation"""
        if self.bow == True:

            """X axis set to False to prevent the character from moving when performing the bow animation"""
            self.movement_x = [False,False]

            self.action, self.action_divider = 'Bow', 3
            self.image = animate_character(self.action)[self.action_divider][self.frame_index]

            if pygame.time.get_ticks() - self.bow_start_time > self.bow_duration:
                self.bow = False
                self.bow_start_time = None

                if pygame.key.get_pressed()[pygame.K_a]:
                    self.movement_x[0] = True
                    self.flip = True

                if pygame.key.get_pressed()[pygame.K_d]:
                    self.movement_x[1] = True
                    self.flip = False

        """Arrow animation"""
        if self.bow == False and self.arrow == True:
            """self.arrow_direction corresponds to the current self.flip state"""
            if not self.arrow_direction:
                self.arrow_x += 30
            else:
                self.arrow_x -= 30
            animate_arrow(self.arrow_direction, self.arrow_x, self.arrow_y)










