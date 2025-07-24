"""
Unit tests for AppState
"""

import unittest

from src.app_state import AppState


class TestAppState(unittest.TestCase):
    def setUp(self):
        """Setup function to run before each test"""
        self.app_state = AppState()

    def test_initial_state(self):
        """Initial state test"""
        self.assertFalse(self.app_state.get("is_running"))
        self.assertEqual(self.app_state.get("current_word"), "")
        self.assertEqual(self.app_state.get("current_text"), "")

    def test_set_get_state(self):
        """State variable set/get test"""
        self.app_state.set("test_key", "test_value")
        self.assertEqual(self.app_state.get("test_key"), "test_value")

    def test_add_letter(self):
        """Add letter test"""
        self.app_state.add_letter("A")
        self.assertEqual(self.app_state.get("current_word"), "A")
        self.assertEqual(self.app_state.get("last_added_letter"), "A")

    def test_add_space(self):
        """Add space test"""
        self.app_state.add_letter("A")
        self.app_state.add_space()
        self.assertEqual(self.app_state.get("current_text"), "A ")
        self.assertEqual(self.app_state.get("current_word"), "")

    def test_delete_last_letter(self):
        """Delete last letter test"""
        self.app_state.add_letter("A")
        self.app_state.add_letter("B")
        self.app_state.delete_last_letter()
        self.assertEqual(self.app_state.get("current_word"), "A")

    def test_clear(self):
        """Clear test"""
        self.app_state.add_letter("A")
        self.app_state.clear()
        self.assertEqual(self.app_state.get("current_word"), "")
        self.assertEqual(self.app_state.get("current_text"), "")

    def test_get_display_text(self):
        """Display text test"""
        self.app_state.add_letter("A")
        self.app_state.add_space()
        self.app_state.add_letter("B")
        self.assertEqual(self.app_state.get_display_text(), "A B")


if __name__ == "__main__":
    unittest.main()
