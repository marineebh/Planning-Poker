# /planning_poker/tests/test_app.py
import unittest
from unittest.mock import MagicMock, patch
from app.utils import load_backlog, save_backlog, calculate_rule_result, Button
import pygame
from unittest import TestCase
from unittest.mock import mock_open, patch
import json


class TestUtils(unittest.TestCase):
    def test_load_backlog_valid(self):
        """Test loading a valid backlog."""
        with patch("builtins.open", unittest.mock.mock_open(read_data='{"Task1": 5, "Task2": 8}')):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {"Task1": 5, "Task2": 8})

    def test_load_backlog_invalid_file(self):
        """Test loading backlog from a non-existing file."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {})

    def test_load_backlog_invalid_json(self):
        """Test loading a backlog with invalid JSON content."""
        with patch("builtins.open", unittest.mock.mock_open(read_data="{invalid_json")):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_save_backlog(self, mocked_file):
        backlog = {"Task1": 5}
        save_backlog('dummy_path', backlog)  # Replace with the actual function call
        mocked_file().write.assert_called_once_with(json.dumps(backlog))


    def test_calculate_rule_result_unanimity_success(self):
        """Test calculate_rule_result with unanimity."""
        votes = {"Player1": 5, "Player2": 5}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, 5)

    def test_calculate_rule_result_unanimity_failure(self):
        """Test calculate_rule_result when votes are not unanimous."""
        votes = {"Player1": 5, "Player2": 8}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, -1)

    def test_calculate_rule_result_median(self):
        """Test calculate_rule_result with median rule."""
        votes = {"Player1": 5, "Player2": 8, "Player3": 3}
        result = calculate_rule_result(votes, "Médiane")
        self.assertEqual(result, 5)

    def test_calculate_rule_result_average(self):
        """Test calculate_rule_result with average rule."""
        votes = {"Player1": 5, "Player2": 8, "Player3": 3}
        result = calculate_rule_result(votes, "Moyenne")
        self.assertEqual(result, 5.33)

    def test_calculate_rule_result_empty_votes(self):
        """Test calculate_rule_result with empty votes."""
        votes = {}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, -1)


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(100, 100, 200, 50, "Test")

    def tearDown(self):
        pygame.quit()

    def test_button_draw(self):
        """Test that the button is drawn."""
        self.button.draw(self.screen)
        pygame.display.flip()  # To render the button visually (not validated here programmatically)

    def test_button_is_clicked_true(self):
        """Test the is_clicked method for a valid click."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
        self.assertTrue(self.button.is_clicked(event))

    def test_button_is_clicked_false(self):
        """Test the is_clicked method for a click outside the button."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (50, 50), "button": 1})
        self.assertFalse(self.button.is_clicked(event))


if __name__ == "__main__":
    unittest.main()
