import sys
import pygame
import os
from Images.images import img_paths
from Main.player import PlayerCharacter

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1792, 1024))
        pygame.display.set_caption("FlashJump")
        self.clock = pygame.time.Clock()
        self.bg_img = pygame.image.load(img_paths["BG_image"]).convert()
        self.player = PlayerCharacter(500,500)

    def run(self,test_case = False):
        """Setting up the test case scenario to a limited number of loop iterations."""
        max_iterations = 5
        iteration = 0

        while True and iteration < max_iterations:

            """Main background image"""
            self.screen.blit(self.bg_img, (0,0))

            """Y axis position"""
            # self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 5
            self.player.img_pos[1] += (self.player.movement_y[1] - self.player.movement_y[0]) * 5
            """X axis position"""
            # self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * 5
            self.player.img_pos[0] += (self.player.movement_x[1] - self.player.movement_x[0]) * 5

            # img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], self.character_img.get_width(), self.character_img.get_height())
            img_rect = pygame.Rect(self.player.img_pos[0], self.player.img_pos[1], self.player.character_img.get_width(), self.player.character_img.get_height())

            self.screen.blit(self.player.character_img, self.player.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    """Y axis"""
                    if event.key == pygame.K_w:
                        self.player.movement_y[0] = True
                    if event.key == pygame.K_s:
                        self.player.movement_y[1] = True
                    """X axis"""
                    if event.key == pygame.K_a:
                        self.player.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.player.movement_x[1] = True

                if event.type == pygame.KEYUP:
                    """Y axis"""
                    if event.key == pygame.K_w:
                        self.player.movement_y[0] = False
                    if event.key == pygame.K_s:
                        self.player.movement_y[1] = False
                    """X axis"""
                    if event.key == pygame.K_a:
                        self.player.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.player.movement_x[1] = False

            pygame.display.update()
            self.clock.tick(60)
            if test_case == True:
                iteration += 1


if __name__ == "__main__":
    Game().run()