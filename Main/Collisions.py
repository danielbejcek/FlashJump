import pygame
screen = pygame.display.set_mode((1792, 1024))

def draw_floor():
    # screen.fill((0,201,120))
    return pygame.draw.line(screen,(0,0,0),(0,924),(1792,924))

