import pygame

def platform_collision(character_pos, character_img):
    floor = pygame.Rect(0, 892, 1792, 100)
    floor_platform = floor.top

    character_rect = character_img.get_rect(topleft=character_pos)

    # pygame.draw.rect(screen, (0, 0, 0,), floor)
    # if character_rect.colliderect(floor):
    #     pygame.draw.rect(screen, (255, 0, 0,), floor)
    # else:
    #     pygame.draw.rect(screen, (0, 0, 0,), floor)
    return floor_platform

