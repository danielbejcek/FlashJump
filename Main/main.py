import sys
import pygame
import os
from Images.images import draw_background
from Main.player import PlayerCharacter
from Main.collisions import Collisions
from Main.enemy import EnemyCharacter


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FlashJump")
        self.clock = pygame.time.Clock()
        self.player = PlayerCharacter()
        self.enemy = EnemyCharacter()
        self.collide = Collisions()
        self.screen = self.player.screen
        self.player_hitbox = None
        self.enemy_hitbox = None

    def run(self,test_case=False, max_iterations=50):
        """Setting up a test case scenario to a limited number of iterations"""
        iteration = 0

        while True and iteration < max_iterations:
            """Main images function"""
            draw_background()

            """Manually drawn hitbox for more responsive collision"""
            player_hitbox = self.player.update_hitbox(self.player.img_pos[0],self.player.img_pos[1])
            self.player_hitbox = pygame.draw.rect(self.screen, (255, 0, 0), player_hitbox, 1)
            # self.player_hitbox = pygame.Rect(player_hitbox)


            """Method that checks for vertical collision and adjusts the character position accordingly"""
            self.collide.check_vertical_collision(self.player_hitbox, self.player,type="player")


            """Controls the movement of the player character"""
            self.player.player_movement()

            """Main method for updating the character's animation (Idle, running, jumping, shooting from a bow)"""
            self.player.update_player_animation()


            """Enemy loop"""
            enemy_hitbox = self.enemy.update_enemy_hitbox(self.enemy.enemy_img_pos[0], self.enemy.enemy_img_pos[1])
            self.enemy_hitbox = pygame.draw.rect(self.screen,(255,0,0),enemy_hitbox,1)
            # self.enemy_hitbox = pygame.Rect(enemy_hitbox)
            self.enemy.draw_enemy()
            self.enemy.enemy_movement()
            self.enemy.update_enemy_animation()
            self.collide.check_vertical_collision(self.enemy_hitbox,self.enemy,type="enemy")



            """Arrow object animation, method is called only when 'arrow_quiver' list is not empty"""
            if self.player.arrow_quiver != []:
                self.player.draw_arrow()

            """Player character image"""
            self.player.draw_player()


            pygame.display.update()
            self.clock.tick(60)

            """Boolean that allows to run only limited number of iterations to perform necessary tests"""
            if test_case == True:
                iteration += 1


if __name__ == "__main__":
    Game().run()