import os
import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock
import pygame
import sys
from Main import main
from Images.images import img_paths
from Images import images
from Main.player import PlayerCharacter
from Main.player_animation import animate_character


current_dir = os.path.dirname(__file__)

class TestGameWindow(unittest.TestCase):

    def setUp(self):
        self.game = main.Game()

    def tearDown(self):
        pass


    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_window_opening(self, mock_pygame_init, mock_set_mode, mock_set_caption):
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

        # Assert that pygame.init() was called
        mock_pygame_init.assert_called_once()
        mock_set_mode.assert_called_once_with((1792, 1024))
        mock_set_caption.assert_called_once_with("FlashJump")


class TestCharacterMovement(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.player = PlayerCharacter(600,500)

        # Setting up x, y position from the player instance in the main.Game()
        self.img_pos = self.game.player.img_pos

        # Setting up x, y position from PlayerCharacter class
        self.initial_pos = self.player.img_pos
    def tearDown(self):
        pass

    @patch('pygame.event.get')
    def test_movement_jump(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_SPACE)]
        self.game.run(True)
        self.assertGreater(self.img_pos[1],self.initial_pos[1])


    @patch('pygame.event.get')
    def test_movement_left(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_a)]
        self.game.run(True)
        self.assertLess(self.img_pos[0], self.initial_pos[0])


    @patch('pygame.event.get')
    def test_movement_right(self, mock_get_event):
        mock_get_event.return_value = [self.simulate_key_press(pygame.K_d)]
        self.game.run(True)
        self.assertGreater(self.img_pos[0], self.initial_pos[0])


    def simulate_key_press(self, key):
        mock_event_key = MagicMock()
        mock_event_key.type = pygame.KEYDOWN
        mock_event_key.key = key
        return mock_event_key

class TestAnimationLists(unittest.TestCase):
    def setUp(self):
        self.actions_list = ['Idle','Running','Jump','Bow']

    """Test that 'animate_character' infact returns a list and that nested lists are being populated with images"""
    def test_animate_character(self):
        for action in self.actions_list:
            result = animate_character(action)
            self.assertIsInstance(result,list)
            self.assertTrue(len(result) > 6)

            """Verify that objects in image lists are pygame.Surface"""
            for image_lists in result:
                for image in image_lists:
                    self.assertIsInstance(image, pygame.Surface)
