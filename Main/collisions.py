import pygame

# def platform_collision(screen,character_pos, character_img):
def platform_collision():
    platform_list = []
    lamp = pygame.Rect(1002, 748, 185, 1)
    floor = pygame.Rect(0, 900, 1792, 1)

    platform_list.append(lamp)
    platform_list.append(floor)

    return platform_list

