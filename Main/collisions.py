import pygame

def platform_collision():
    platform_list = []
    floor = pygame.Rect(0, 900, 1792, 2)
    lamp = pygame.Rect(1002, 748, 185, 2)
    right_roof = pygame.Rect(1348, 626, 200, 2)
    chimney = pygame.Rect(1660, 464, 100, 2)
    second_right_roof = pygame.Rect(1375, 351, 150, 2)
    tent = pygame.Rect(511, 756, 290, 2)
    sky_platform_right = pygame.Rect(958, 281, 175, 2)
    sky_platform_left = pygame.Rect(555, 281, 175, 2)
    sky_platform_bottom = pygame.Rect(555, 452, 175, 2)
    left_roof = pygame.Rect(145, 622, 290, 2)

    platform_list.append(floor)
    platform_list.append(lamp)
    platform_list.append(right_roof)
    platform_list.append(chimney)
    platform_list.append(second_right_roof)
    platform_list.append(tent)
    platform_list.append(sky_platform_right)
    platform_list.append(sky_platform_left)
    platform_list.append(sky_platform_bottom)
    platform_list.append(left_roof)

    return platform_list

