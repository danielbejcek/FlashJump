from Core import main
import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock
import pygame
import sys
from Core import main



class TestGameWindow(unittest.TestCase):

    def setUp(self):
        self.ref_images = main.Game().img_paths
        self.test_bg_img = self.ref_images["BG_image"]

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
        self.assertEqual(self.test_bg_img,"..\Images\BG_MAIN.png")




