import pygame

def platform_collision(screen,character_pos, character_img):
    platform_list = []

    lamp = pygame.Rect(1002, 700, 185, 10)
    platform_list.append(lamp)

    floor = pygame.Rect(0, 892, 1792, 10)
    platform_list.append(floor)

    character_rect = character_img.get_rect(topleft=character_pos)

    for collide_point in platform_list:
        if character_rect.colliderect(collide_point):
            if collide_point == floor:
                pygame.draw.rect(screen, (255, 0, 0,), floor)
            elif collide_point == lamp:
                pygame.draw.rect(screen, (255, 0, 0,), lamp)
        else:
            pygame.draw.rect(screen, (0, 0, 0,), floor)
            pygame.draw.rect(screen, (0, 0, 0,), lamp)
    return platform_list

