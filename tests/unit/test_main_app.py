import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.exceptions import YasminBaseException
from src.main_app import SignLanguageApp


class TestMainApp(unittest.TestCase):
    def setUp(self):
        """Setup function to run before each test"""
        # Create Tkinter root window
        self.root = tk.Tk()
        self.ui_class = MagicMock()
        self.app = SignLanguageApp(self.root, self.ui_class)

    def tearDown(self):
        """Cleanup function to run after each test"""
        if hasattr(self, "app"):
            self.app.quit_app()
        if hasattr(self, "root") and self.root.winfo_exists():
            self.root.destroy()

    def test_app_state_management(self):
        """Application state management tests"""
        # Check initial state
        self.assertFalse(self.app.state.get("is_running"))

        # Check running state change
        self.app.state.set("is_running", True)
        self.assertTrue(self.app.state.get("is_running"))

        self.app.state.set("is_running", False)
        self.assertFalse(self.app.state.get("is_running"))


if __name__ == "__main__":
    unittest.main()
