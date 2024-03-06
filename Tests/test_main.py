import os
import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock
import pygame
from Main import main
from Main.player import PlayerCharacter
from Main.player_animation import animate_character
from Main.collisions import platform_collision


current_dir = os.path.dirname(__file__)

class TestGameWindow(unittest.TestCase):

    def setUp(self):
        self.game = main.Game()

    def tearDown(self):
        pass


    @patch('pygame.display.set_caption')
    @patch('pygame.init')
    def test_window_opening(self, mock_pygame_init, mock_set_caption):
        """
        'mock_event' is a mock object to simulate a Pygame event. 
        In the context of this test, we're specifically creating a mock event that simulates the pygame.QUIT event. 
        This is the kind of event that would be generated when a user tries to close the game window.
        When the main() function is called within this with block, every time it reaches pygame.event.get(),
        instead of getting the actual events from the Pygame event queue, it gets the mocked list [mock_event] we provided.
        Since mock_event is set up to mimic a pygame.QUIT event, the main loop will behave as if the user is trying to close the window,
        triggering the condition to exit the loop and allowing your test to proceed without getting stuck in an infinite loop.
        """

        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        with patch('pygame.event.get', return_value=[mock_event]):
            try:
                main.Game()

            except SystemExit:
               pass

        """Assert that 'pygame.init()' was called"""
        mock_pygame_init.assert_called_once()
        mock_set_caption.assert_called_once_with("FlashJump")


class TestCharacterMovement(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()

        """Instance of player from PlayerCharacter class"""
        self.player = PlayerCharacter(600,700)

        """Instance from main game loop"""
        self.game.player = PlayerCharacter(600,700)

        """Setting up x, y position from the player instance in the main.Game() which is being updated"""
        self.game_pos = self.game.player.img_pos

        self.hitbox = self.game.player.hitbox

        """Setting up x, y position from static PlayerCharacter class"""
        self.initial_pos = self.player.img_pos

        """Setting up a floor collision object"""
        self.floor_platform = platform_collision()[1]


    def tearDown(self):
        pass

    @patch('pygame.event.get')
    def test_movement_jump(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_SPACE)]
        self.game.run(True,100)
        self.assertLess(self.game_pos[1],self.initial_pos[1])
        self.assertTrue(self.game.player.jump)
        self.assertFalse(self.game.player.movement_y[1])
        self.assertTrue(self.game.player.movement_y[0])

        """Variables that are bound to be set to False while jump animation is active"""
        self.assertFalse(self.game.player.peak)
        self.assertFalse(self.game.player.bow)
        self.assertFalse(self.game.player.attack)


    @patch('pygame.event.get')
    def test_movement_left(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_a)]
        self.game.run(True)
        self.assertLess(self.game_pos[0], self.initial_pos[0])
        self.assertTrue(self.game.player.movement_x[0])
        self.assertFalse(self.game.player.movement_x[1])

    @patch('pygame.event.get')
    def test_movement_right(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_d)]
        self.game.run(True)
        self.assertGreater(self.game_pos[0], self.initial_pos[0])
        self.assertTrue(self.game.player.movement_x[1])
        self.assertFalse(self.game.player.movement_x[0])

    @patch('pygame.event.get')
    def test_bow_animation(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_e)]
        self.game.run(True)
        self.assertFalse(self.game.player.movement_x[0])
        self.assertFalse(self.game.player.movement_x[1])
        self.assertTrue(self.game.player.bow)
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_q)]
        self.assertFalse(self.game.player.attack)

    @patch('pygame.event.get')
    def test_attack_animation(self, mock_get_event):
        self.game_pos[1] = 600
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_q)]
        self.game.run(True)
        self.assertFalse(self.player.movement_x[0])
        self.assertFalse(self.player.movement_x[1])
        self.assertTrue(self.game.player.attack)


    def simulate_key_press(self, key):
        mock_event_key = MagicMock()
        mock_event_key.type = pygame.KEYDOWN
        mock_event_key.key = key
        return mock_event_key

class TestAnimationLists(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        """Instance of player from PlayerCharacter class"""
        self.player = PlayerCharacter(600, 500)

        """Setting up x, y position from the player instance in the main.Game() which is being updated"""
        self.img_pos = self.game.player.img_pos

        """Setting up x, y position from static PlayerCharacter class"""
        self.initial_pos = self.player.img_pos

        """Action list to simulate animations"""
        self.actions_list = ['Idle','Running','Jump','Bow','Attack_1','Attack_2','Landing']

        self.mock_surface = pygame.Surface((1,1))


    def tearDown(self):
        pass

    """Test that 'draw_character' is called with proper arguments"""
    @patch('pygame.transform.flip')
    def test_draw_character(self,mock_flip):

        self.player.screen = MagicMock()

        self.player.image = pygame.Surface((1,1))

        mock_flip.return_value = self.mock_surface

        self.player.draw_character()
        mock_flip.assert_called_with(self.player.image, self.player.flip, False)
        self.player.screen.blit.assert_called_with(self.mock_surface, self.player.img_pos)

    """Test that 'animate_character' in fact returns a list and that nested lists are being populated with images"""
    def test_animate_character(self):
        for action in self.actions_list:
            result = animate_character(action)
            self.assertIsInstance(result,list)
            self.assertTrue(len(result) > 1)

            """Verify that objects in image lists are pygame.Surface"""
            for image_lists in result:
                for image in image_lists:
                    self.assertIsInstance(image, pygame.Surface)
    def test_create_arrow(self):
        """Starting with an empty list"""
        self.assertListEqual([],self.player.arrow_quiver)

        """Method call"""
        self.player.create_arrow()

        """Length of nested list after first method call"""
        self.assertEqual(len(self.player.arrow_quiver[0]),5)

        self.assertFalse(self.player.flip)

        """Length of parent list should be 2 after we call 'create_arrow' twice"""
        for i in range(10):
            self.player.create_arrow()
        self.assertEqual(len(self.player.arrow_quiver),11)



    def test_draw_arrow_called(self):
        """
        Calling the 'create_arrow' method in the main loop to populate list with arrow objects and verify,
        that 'draw_arrow' method is being accurately called only if the 'arrow_quiver' is not empty.
        """
        self.game.player.create_arrow()
        with patch.object(PlayerCharacter,'draw_arrow') as mock_draw_arrow:
            self.game.run(True)
        mock_draw_arrow.assert_called()

        """Setting up a list with 20 arrows to be removed if 'player.draw_arrow' works as intended"""
        for i in range(20):
            self.game.player.create_arrow()
        self.assertEqual(len(self.game.player.arrow_quiver),21)
        """
        Integration test to simulate removal of the arrows from the 'arrow_quiver'. 
        After we created 20 arrows, it takes 5 iterations to completely remove them from the list.
        """
        with patch('pygame.time.get_ticks') as mock_time:
            """
            With 'pygame.time.get_ticks' mock we allow the arrow fly animation to complete.
            We are effectively setting the mocked time to 10 seconds, meaning 10 seconds have passed in the test scenario.
            """
            mock_time.return_value = 20000
            self.game.run(True)
            print(len(self.game.player.arrow_quiver),"Arrows left in quiver")
            self.assertEqual(len(self.game.player.arrow_quiver),0)


class TestCollisionList(unittest.TestCase):
    def setUp(self) -> None:
        self.game = main.Game()

        """Setting up a collision objects from 'platform_collision' function that returns a list"""
        self.floor_platform = platform_collision()[0]
        self.lamp_platform = platform_collision()[1]
        self.roof_platform = platform_collision()[2]
        self.chimney_platform = platform_collision()[3]
        self.second_roof_platform = platform_collision()[4]
        self.tent_platform = platform_collision()[5]


    def tearDown(self) -> None:
        pass

    """
    Test how the character reacts to collision after being dropped from Y coordinate to a certain type of collision object.
    """
    def test_collision_floor(self):
        self.game.player.img_pos = [200,500]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.floor_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.floor_platform.top - self.game.player.image.get_height(), 5)


    def test_collision_lamp(self):
        self.game.player.img_pos = [1000,400]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.lamp_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.lamp_platform.top - self.game.player.image.get_height(), 5)

    def test_collision_roof(self):
        self.game.player.img_pos = [1300,300]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.roof_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.roof_platform.top - self.game.player.image.get_height(), 5)

    def test_collision_chimney(self):
        self.game.player.img_pos = [1650,50]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.chimney_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.chimney_platform.top - self.game.player.image.get_height(), 5)

    def test_collision_second_roof(self):
        self.game.player.img_pos = [1350,0]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.second_roof_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.second_roof_platform.top - self.game.player.image.get_height(), 5)

    def test_collision_tent(self):
        self.game.player.img_pos = [500,300]
        self.assertFalse(self.game.player.touchdown)
        self.assertNotEqual(self.game.player.img_pos[1], self.tent_platform.top - self.game.player.image.get_height())
        self.game.run(True)
        self.assertTrue(self.game.player.touchdown)
        self.assertAlmostEqualsInt(self.game.player.img_pos[1],self.tent_platform.top - self.game.player.image.get_height(), 5)

    """
    Custom method to test that after player has landed,
    the difference between the player position and the collision floor is not more than 5 pixels.
    """
    def assertAlmostEqualsInt(self, first, second, delta):
        if delta >= 5:
            self.assertTrue(abs(first - second) <= delta)
        else:
            self.fail("Delta is not great enough")

