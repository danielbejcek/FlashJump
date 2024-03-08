import pygame
import sys
from Images.images import img_paths
from Main.player_animation import animate_character



class PlayerCharacter(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1792, 1024))
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        """Character is starting in an 'Idle' animation"""
        self.action = 'Idle'

        """Serves as a divider between actions. 0 is for idle, 1 is for running etc..."""
        self.action_divider = 0

        """Initial image object"""
        self.image = pygame.Surface((0, 0))

        """'self.frame_index' serves to access the specific image as an index in a 'animation_list' received from 'animate_character' function."""
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        """Main movement variables"""
        self.movement_y = [False, True]
        self.movement_x = [False, False]
        self.img_pos = [x, y]
        self.flip = False
        self.y_velocity = 8
        self.x_velocity = 5
        self.drop_platform = pygame.Rect(0, 0, 0, 0)

        """Jump animation variables"""
        self.jump = False
        self.touchdown = False
        self.jump_height = 180
        self.jump_init_pos = None
        self.peak = False
        self.descent = False

        """Bow animation variables"""
        self.bow = False
        self.bow_start_time = None
        self.bow_duration = 650

        """Attack animation variables"""
        self.attack = False
        self.attack_animation = 'Attack_1'
        self.attack_start_time = None
        self.attack_duration = 700

        """Arrow object variables"""
        self.arrow = False
        self.arrow_y = self.img_pos[1] - (self.image.get_height() - 30)
        self.arrow_x = self.img_pos[0]
        self.arrow_direction = True
        self.arrow_quiver = []
        self.arrow_duration = 3000

        """Hitbox"""
        self.hitbox = None

        """
        Variables that help control the movement of the character. When user presses 'Key_A' to run left and right after 'Key_D' to run right,
        character will stop and enter 'Idle' animation, until one of the keys is released.
        """
        self.motion_left = False
        self.motion_right = False

    """Creating a custom hitbox to better control the character collisions"""
    def update_hitbox(self,x,y):
        self.hitbox = (x + 63, y + 71,30,90)
        return self.hitbox

    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.img_pos)

    """Main method of the player's movement apparatus"""
    def player_movement(self):
        """X axis position"""
        self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * self.x_velocity

        """Y axis position"""
        self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * self.y_velocity



        """Main player animation loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """Controls for player when character is touching the ground"""
            if self.touchdown == True:
                if event.type == pygame.KEYDOWN and not any([self.bow, self.attack]):


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
                        self.touchdown = False
                        self.y_velocity = 8
                        self.jump_init_pos = self.img_pos[1]


                    """Bow animation"""
                    if event.key == pygame.K_e:
                        self.bow = True
                        self.frame_index = 0
                        self.bow_start_time = pygame.time.get_ticks()

                        """Arrow object orientation"""
                        self.arrow_direction = self.flip
                        if self.flip:
                            self.arrow_x = self.img_pos[0]
                        if not self.flip:
                            self.arrow_x = self.img_pos[0]

                    """Attack animation"""
                    if event.key == pygame.K_q:
                        self.attack = True
                        self.frame_index = 0
                        self.attack_start_time = pygame.time.get_ticks()

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

            """Jump action movement control"""
            if self.touchdown == False and not any([self.bow, self.attack]):
                if event.type == pygame.KEYDOWN:

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

    """
    Method that checks for character's vertical position. 
    Whenever the player is touching the ground, 'self.touchdown' is set to True.
    Whenever player proceeds to press the SPACE button, 'self.touchdown' is set to False.
    The main movement of the character's apparatus is changing according to this variable
    """
    def check_vertical_collision(self, platforms, hitbox):
        """
        self.touchdown is set to False at the beginning of the method.
        If a collision is detected, it is set to True. If no collision occurs, it remains False.
        Method is being updated in every frame of the loop to ensure proper collision functionality.
        """

        self.touchdown = False
        for platform in platforms:
            # pygame.draw.rect(self.screen, (255, 0, 0,), platform)

            """
            Once collision hitbox is met with one of the platform objects, 
            vertical variables are set accordingly for the player to be able to use the platform.
            """
            if hitbox.colliderect(platform) and self.descent == False:
                if self.jump == False:
                    self.y_velocity = 8
                    self.movement_y[1] = False
                    self.img_pos[1] = platform.top - self.image.get_height()
                    self.peak = False
                    self.touchdown = True
                    self.action, self.action_divider = 'Idle', 0
                    # pygame.draw.rect(self.screen, (100, 100, 100,), platform)

                    if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                        self.action, self.action_divider = 'Running', 1

                    if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]:
                        self.action, self.action_divider = 'Idle', 0



            """
            Whenever player wants to descent and presses the 'S' key, current platform is stored in 'self.drop_platform' variable, 
            usable only when colliding with platform -> 'self.touchdown == True'.
            If player is on floor platform, condition will not be triggered.
            """
            if pygame.key.get_pressed()[pygame.K_s] and self.touchdown == True:
                if platform == platforms[0]:
                    self.descent = False
                else:
                    self.drop_platform = platform
                    self.descent = True

            """
            Once 'self.descent' is set to True, player will disengage from the current platform and drop one level lower.
            Once the player's hitbox is no longer within the collision range of 'self.drop_platform', 'self.descent' is again set to False
            to allow regular collision with platforms bellow.
            """
            if self.descent == True:
                if hitbox.colliderect(self.drop_platform):
                    self.touchdown = False
                    self.movement_y[1] = True
                else:
                    self.descent = False
                    self.movement_y[1] = False
                    self.touchdown = True

        """
        If jump animation is not detected, character will now perform a 'Landing' animation,
        as he is falling from the edge of the collision platform towards the ground.
        """
        if not self.touchdown:
            if not self.jump:
                self.movement_y[1] = True
                self.peak = True
                self.action, self.action_divider = 'Landing', 6


    def update_animation(self):
        """
        self.image controls the image generator. We are accessing the list which is returned from animate_character function.
        We pass 'self.action_divider' that controls the nature of the action (idle, running etc...) 
        and 'self.frame_index' which allows the animation to always start from index 0 whenever a new action is introduced to prevent a 'list index out of range'.
        """

        self.image = animate_character(self.action)[self.action_divider][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > 80:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        """Once 'self.frame_index' reaches the final element in the 'animation_list', it starts over from index 0 to maintain fluent animation."""
        if self.frame_index >= len(animate_character(self.action)[self.action_divider]):
            self.frame_index = 0

        """Jump animation configuration"""
        if self.jump:
            if not self.peak:
                """'self.peak' defines a final point of the jump animation, 'self.y_velocity' is decreasing until this point is reached"""
                if self.img_pos[1] >= (self.jump_init_pos - self.jump_height):
                    self.y_velocity -= .15
                    self.action, self.action_divider = 'Jump', 2
                    self.movement_y[0] = True
                    self.movement_y[1] = False

                """Breakpoint of the climb, resets the 'self.jump' animation back to False"""
                if self.img_pos[1] <= (self.jump_init_pos - self.jump_height):
                    self.peak = True
                    self.jump = False

        """Once player reaches the 'self.peak', descending sequence is initialized, increasing the falling speed"""
        if self.peak:
            self.y_velocity += .5
            self.action, self.action_divider = 'Landing', 6
            self.movement_y[0] = False
            self.movement_y[1] = True

        """Attack animation"""
        if self.attack:
            """X axis set to False to prevent the character from moving when performing the attack animation"""
            self.movement_x = [False, False]
            self.action, self.action_divider = self.attack_animation, 4
            self.image = animate_character(self.action)[self.action_divider][self.frame_index]

            """Condition is triggered after the attack animation is finished"""
            if pygame.time.get_ticks() - self.attack_start_time > self.attack_duration:
                self.attack = False
                self.attack_start_time = None

                """Clears the pygame key input queue in case the 'Q' key remains pressed, preventing looping of the animation"""
                pygame.event.clear()

                """Condition that switches between two types of attack animation"""
                if self.attack_animation == 'Attack_1':
                    self.action, self.action_divider = self.attack_animation, 5
                    self.attack_animation = 'Attack_2'
                else:
                    self.attack_animation = 'Attack_1'

                """Helper conditions that allow fluent movement if any of the direction keys is pressed while performing the attack"""
                if not pygame.key.get_pressed()[pygame.K_q]:
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.movement_x[1] = True
                        self.motion_right = True
                        self.flip = False

                    if pygame.key.get_pressed()[pygame.K_a]:
                        self.movement_x[0] = True
                        self.motion_left = True
                        self.flip = True

                if pygame.key.get_pressed()[pygame.K_q]:
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.movement_x[1] = True
                        self.motion_right = True
                        self.flip = False

                    if pygame.key.get_pressed()[pygame.K_a]:
                        self.movement_x[0] = True
                        self.motion_left = True
                        self.flip = True

        """Bow animation"""
        if self.bow == True:

            """X axis set to False to prevent the character from moving when performing the bow animation"""
            self.movement_x = [False, False]
            self.flip = self.arrow_direction
            self.action, self.action_divider = 'Bow', 3
            self.image = animate_character(self.action)[self.action_divider][self.frame_index]

            """Condition is triggered after the bow animation is finished"""
            if pygame.time.get_ticks() - self.bow_start_time > self.bow_duration:
                self.bow = False
                self.arrow = True
                self.bow_start_time = None

                """If key 'E' is held down, the bow animation keeps going as well as the projectiles"""
                if pygame.key.get_pressed()[pygame.K_e]:
                    self.motion_left = False
                    self.motion_right = False
                    self.bow = True
                    self.bow_start_time = pygame.time.get_ticks()

                if pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_e]:
                    self.movement_x[1] = True
                    self.motion_right = True
                    self.flip = False

                if pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_e]:
                    self.movement_x[0] = True
                    self.motion_left = True
                    self.flip = True

                """Arrow animation"""
                if self.arrow == True:
                    self.create_arrow()
                    self.arrow = False


    def create_arrow(self):
        self.arrow_start_time = pygame.time.get_ticks()
        arrow_default = pygame.image.load(img_paths['arrow_default'])
        arrow_scaled = pygame.transform.scale(arrow_default, (int(arrow_default.get_width() * 1.3), (int(arrow_default.get_height() * 1.3))))
        arrow_image = pygame.transform.flip(arrow_scaled, self.arrow_direction, False)

        """Each arrow instance is stored in a 'arrow_quiver' list to enable firing multiple arrows without overlapping"""
        self.arrow_quiver.append([arrow_image,self.arrow_direction,self.arrow_x,self.arrow_y, self.arrow_start_time])


    def draw_arrow(self):
        """
        'arrow_quiver' list contains multiple items to help us control the arrow object.
        - arrow_quiver[0] - pygame.Surface image of an arrow.
        - arrow_quiver[1] - Boolean that derives from 'self.flip', which gives us direction in which the arrow will fly.
        - arrow_quiver[2] - integer X axis position which is being constantly updated while in the loop to simulate animation.
        - arrow_quiver[3] - static integer Y axis position to vertically place the arrow where character currently is.
        - arrow_quiver[4] - pygame.time.get_ticks() method to help us track the life span of each individual arrow.
        """
        for index, arrow in enumerate(self.arrow_quiver):
            """Direction is left"""
            if arrow[1] == True:
                arrow[2] -= 15
                """After 'arrow_duration' has passed, arrow image will be not be active in the main loop anymore"""
                if pygame.time.get_ticks() - arrow[4] < self.arrow_duration:
                    self.screen.blit((arrow[0]), (arrow[2], arrow[3]))
                else:
                    self.arrow_quiver.pop(index)

            """Direction is right"""
            if arrow[1] == False:
                arrow[2] += 15
                if pygame.time.get_ticks() - arrow[4] < self.arrow_duration:
                    self.screen.blit((arrow[0]), (arrow[2] + 100, arrow[3]))
                else:
                    self.arrow_quiver.pop(index)

