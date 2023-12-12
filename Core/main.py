import sys
import pygame



def _main():
    pygame.init()
    pygame.display.set_mode((1792, 1024))
    pygame.display.set_caption("FlashJump")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    _main()