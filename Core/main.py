import sys
import pygame


class Game:
    def __init__(self):
        self.img_paths = {
            "BG_image": "D:\Documents\PyCharm projects\PyCharm projects\PyGame\FlashJump\Images\BG_MAIN.png",
            "particle_img1": "D:\Documents\PyCharm projects\PyCharm projects\PyGame\FlashJump\Images\Particles\leaf_particle_1.png",
            "character_img": "D:\Documents\PyCharm projects\PyCharm projects\PyGame\FlashJump\Images\Character\character.png",

        }
        pygame.init()
        self.screen = pygame.display.set_mode((1792, 1024))
        pygame.display.set_caption("FlashJump")
        self.clock = pygame.time.Clock()

        self.bg_img = pygame.image.load(self.img_paths["BG_image"])
        self.character_img = pygame.image.load(self.img_paths["character_img"])

        self.movement_y = [False, False]
        self.movement_x = [False, False]
        self.img_pos = [160,260]
        self.collision_area = pygame.Rect(200,100,100,100)

    def run(self):

        while True:
            self.screen.blit(self.bg_img, (0,0))

            self.img_pos[1] += (self.movement_y[1] - self.movement_y[0]) * 5
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
                    """Y Axis"""
                    if event.key == pygame.K_w:
                        self.movement_y[0] = True
                    if event.key == pygame.K_s:
                        self.movement_y[1] = True
                    """X Axis"""
                    if event.key == pygame.K_a:

                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True



                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement_y[0] = False
                    if event.key == pygame.K_s:
                        self.movement_y[1] = False
                    if event.key == pygame.K_a:
                        self.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.movement_x[1] = False


            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()