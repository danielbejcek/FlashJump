import pygame

def platform_collision():
    platform_list = []
    lamp = pygame.Rect(1002, 748, 185, 2)
    floor = pygame.Rect(0, 900, 1792, 2)
    roof = pygame.Rect(1350, 675, 200, 2)

    platform_list.append(lamp)
    platform_list.append(floor)
    platform_list.append(roof)

    return platform_list

