import sys
import pygame
import os
from Images import images
from Main.player import PlayerCharacter
from Main.Collisions import draw_floor


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1792, 1024))
        pygame.display.set_caption("FlashJump")

        self.clock = pygame.time.Clock()
        self.player = PlayerCharacter(600,770)

    def run(self,test_case = False):
        """Setting up a test case scenario to a limited number of iterations."""
        max_iterations = 20
        iteration = 0

        while True and iteration < max_iterations:

            """Main background image"""
            images.screen.blit(images.bg_img, (0,0))

            draw_floor()

            """Main method for updating the character's animation (Idle, running, jumping, shooting from a bow)"""
            self.player.update_animation()

            """Player character image"""
            self.player.draw_character()

            """Controls the movement of the player character"""
            self.player.player_movement()

            pygame.display.update()
            self.clock.tick(60)

            """Boolean that allows to run only limited number of iterations to perform necessary tests"""
            if test_case == True:
                iteration += 1


if __name__ == "__main__":
    Game().run()