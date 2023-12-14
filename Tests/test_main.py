import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock
import pygame
import sys
import os
from Main import main

class TestGameWindow(unittest.TestCase):

    def setUp(self):
        self.original_directory = os.getcwd()
        core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Main')
        os.chdir(core_path)

        self.game = main.Game()
        self.images_ref = self.game.img_paths
        self.test_bg_img = self.images_ref["BG_image"]


    def tearDown(self):
        os.chdir(self.original_directory)

    @patch('pygame.image.load')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_window_opening(self, mock_pygame_init, mock_set_mode, mock_set_caption, mock_load):
        """
        'mock_event' is a mock object to simulate a Pygame event. 
        In the context of this test, we're specifically creating a mock event that simulates the pygame.QUIT event. 
        This is the kind of event that would be generated when a user tries to close the game window.
        When the _main() function is called within this with block, every time it reaches pygame.event.get(),
        instead of getting the actual events from the Pygame event queue, it gets the mocked list [mock_event] we provided.
        Since mock_event is set up to mimic a pygame.QUIT event, the main loop will behave as if the user is trying to close the window,
        triggering the condition to exit the loop and allowing your test to proceed without getting stuck in an infinite loop.
        """
        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        with patch('pygame.event.get', return_value=[mock_event]):
            try:
                main.Game()
                print("Window has been innitialized successfuly.")
            except SystemExit:
               pass


        # Assert that pygame.init() was called
        mock_pygame_init.assert_called_once()
        mock_set_mode.assert_called_once_with((1792, 1024))
        mock_set_caption.assert_called_once_with("FlashJump")

        mock_load.assert_any_call(self.test_bg_img)
        self.assertEqual(self.test_bg_img,"Images\BG_MAIN.png")



if __name__ == "__main__":
    unittest.TestCase()
