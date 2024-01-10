import pygame
import os
from Images.images import img_paths
# from Main.player import PlayerCharacter

current_dir = os.path.dirname(__file__)
screen = pygame.display.set_mode((1792, 1024))
# player = PlayerCharacter(50,50)
def animate_character(action):
    animation_list = []
    temp_list = []


    for i in os.listdir(os.path.join(current_dir,'..','Images','Characters','Player',action)):
        img = pygame.image.load(os.path.join(current_dir,'..','Images','Characters','Player',action,i))
        img = pygame.transform.scale(img, (int(img.get_width() // .8), (int(img.get_height() // .8))))

        if action == 'Idle':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Running':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Jump':
            temp_list.append(img)
            animation_list.append(temp_list)

        if action == 'Bow':
            temp_list.append(img)
            animation_list.append(temp_list)

    return animation_list



def animate_arrow():
    pass
    # player.arrow_quiver
    # arrow_timestamp = pygame.time.get_ticks()
    # arrow_default = pygame.image.load(img_paths['arrow_default'])
    # arrow_scaled = pygame.transform.scale(arrow_default, (int(arrow_default.get_width() * 1.3), (int(arrow_default.get_height() * 1.3))))
    # arrow_image = pygame.transform.flip(arrow_scaled, direction, False)
    # # arrow_object = screen.blit(pygame.transform.flip(arrow_default, direction, False), (x_pos, y_pos))
    #
    # return [arrow_image, x_pos, y_pos,direction]



