import sys
import pygame
import os
from Images.images import img_paths




class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((1792, 1024))
        pygame.display.set_caption("FlashJump")
        self.clock = pygame.time.Clock()

        self.bg_img = pygame.image.load(img_paths["BG_image"]).convert()
        self.character_img = pygame.image.load(img_paths["character_img"])

        self.movement_y = [False, False]
        self.movement_x = [False, False]
        self.img_pos = [160,260]
        self.collision_area = pygame.Rect(200,100,100,100)



    def run(self,test_case = False):
        """Setting up the test case scenario to a limited number of loop iterations."""
        max_iterations = 5
        iteration = 0

        while True and iteration < max_iterations:
            """Main background image"""
            self.screen.blit(self.bg_img, (0,0))

            """Y axis position"""
            self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 5
            """X axis position"""
            self.img_pos[0] += (self.movement_x[1] - self.movement_x[0]) * 5

            img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], self.character_img.get_width(), self.character_img.get_height())

            if img_rect.colliderect(self.collision_area):
                pygame.draw.rect(self.screen,(0,10,255),self.collision_area)
            else:
                pygame.draw.rect(self.screen,(0,50,155),self.collision_area)

            self.screen.blit(self.character_img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    """Y axis"""
                    if event.key == pygame.K_w:
                        self.movement_y[0] = True
                    if event.key == pygame.K_s:
                        self.movement_y[1] = True
                    """X axis"""
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True

                if event.type == pygame.KEYUP:
                    """Y axis"""
                    if event.key == pygame.K_w:
                        self.movement_y[0] = False
                    if event.key == pygame.K_s:
                        self.movement_y[1] = False
                    """X axis"""
                    if event.key == pygame.K_a:
                        self.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.movement_x[1] = False

            pygame.display.update()
            self.clock.tick(60)
            if test_case == True:
                iteration += 1


if __name__ == "__main__":
    Game().run()