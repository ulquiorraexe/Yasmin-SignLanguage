"""
Application State Manager
Manages the state of the sign language translator application.
"""

import logging
import time

logger = logging.getLogger(__name__)


class AppState:
    """Class that manages the application state."""

    def __init__(self):
        """Initializes the application state."""
        self._state = {
            "is_running": False,
            "detected_letter": "",
            "current_word": "",
            "current_text": "",
            "translated_text": "",
            "last_added_letter": None,
            "cap": None,
            "last_detection_time": time.time(),
            "word_timeout": 1.0,  # 1 second gap = new word
        }
        logger.debug("Application state initialized")

    def get(self, key, default=None):
        """Gets a state variable.

        Args:
            key: Variable name
            default: Default value (returned if variable not found)

        Returns:
            Variable value
        """
        return self._state.get(key, default)

    def set(self, key, value):
        """Sets a state variable.

        Args:
            key: Variable name
            value: New value
        """
        self._state[key] = value
        logger.debug(f"State updated: {key} = {value}")

    def update(self, updates):
        """Updates multiple state variables.

        Args:
            updates: Dictionary containing key-value pairs
        """
        self._state.update(updates)
        logger.debug(f"State updated in bulk: {updates}")

    def reset(self):
        """Resets all state variables."""
        self._state = {
            "is_running": False,
            "detected_letter": "",
            "current_word": "",
            "current_text": "",
            "translated_text": "",
            "last_added_letter": None,
            "cap": None,
            "last_detection_time": time.time(),
            "word_timeout": 1.0,
        }
        logger.debug("Application state reset")

    def get_all(self):
        """Returns all state variables.

        Returns:
            dict: A copy of the state
        """
        return self._state.copy()

    def get_display_text(self):
        """Returns the current display text.

        Returns:
            str: Current text
        """
        return self._state["current_text"] + self._state["current_word"]

    def add_letter(self, letter):
        """Adds a letter to the current word.

        Args:
            letter: Letter to add
        """
        self._state["detected_letter"] = letter
        self._state["current_word"] += letter
        self._state["last_detection_time"] = time.time()
        self._state["last_added_letter"] = letter
        logger.debug(
            f"Letter added: {letter}, new word: {self._state['current_word']}"
        )

    def add_space(self):
        """Adds a space to the text."""
        if self._state["current_word"]:
            self._state["current_text"] += self._state["current_word"] + " "
            self._state["current_word"] = ""
        else:
            # Add space even if there is no word
            self._state["current_text"] += " "

        # Allow the same letter to be detected again after a space
        self._state["last_added_letter"] = None
        logger.debug("Space added")

    def delete_last_letter(self):
        """Deletes the last letter."""
        if self._state["current_word"]:
            # Delete last letter from current word
            self._state["current_word"] = self._state["current_word"][:-1]
            # Update last letter
            self._state["last_added_letter"] = (
                None
                if not self._state["current_word"]
                else self._state["current_word"][-1]
            )
            logger.debug("Last letter deleted (from current word)")
        elif self._state["current_text"]:
            # Find the last non-empty word
            self._state["current_text"] = self._state["current_text"].rstrip()

            if self._state["current_text"]:
                parts = self._state["current_text"].rsplit(" ", 1)

                if len(parts) > 1:
                    self._state["current_text"] = parts[0] + " "
                    self._state["current_word"] = parts[1]
                else:
                    self._state["current_word"] = parts[0]
                    self._state["current_text"] = ""

                # Update last letter
                self._state["last_added_letter"] = (
                    None
                    if not self._state["current_word"]
                    else self._state["current_word"][-1]
                )
                logger.debug("Last letter deleted (from previous word)")

    def clear(self):
        """Clears the text content."""
        self._state["detected_letter"] = ""
        self._state["current_word"] = ""
        self._state["current_text"] = ""
        self._state["translated_text"] = ""
        self._state["last_added_letter"] = None
        logger.debug("Text content cleared")
