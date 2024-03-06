import pygame

def platform_collision():
    platform_list = []
    lamp = pygame.Rect(1002, 748, 185, 2)
    floor = pygame.Rect(0, 900, 1792, 2)
    roof = pygame.Rect(1348, 626, 200, 2)
    chimney = pygame.Rect(1660, 462, 100, 2)
    second_roof = pygame.Rect(1375, 350, 150, 2)
    tent = pygame.Rect(511, 756, 290, 2)

    platform_list.append(floor)
    platform_list.append(lamp)
    platform_list.append(roof)
    platform_list.append(chimney)
    platform_list.append(second_roof)
    platform_list.append(tent)

    return platform_list

