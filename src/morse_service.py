"""
Morse Code Service
Manages Morse code operations for the sign language application.
"""

import logging
import time
import winsound

logger = logging.getLogger(__name__)


class MorseCodeService:
    """Service class for Morse code operations."""

    MORSE_CODE_DICT = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
    }

    @classmethod
    def text_to_morse(cls, text):
        """Converts text to Morse code."""
        morse_text = ""
        for char in text.upper():
            if char in cls.MORSE_CODE_DICT:
                morse_text += cls.MORSE_CODE_DICT[char] + " "
            else:
                morse_text += char + " "
        return morse_text

    @classmethod
    def play_morse_code(cls, morse_text):
        """Plays Morse code as sound."""
        dot_duration = 200  # milliseconds
        dash_duration = 3 * dot_duration
        frequency = 800  # Hz

        try:
            for symbol in morse_text:
                if symbol == ".":
                    winsound.Beep(frequency, dot_duration)
                    time.sleep(dot_duration / 1000)  # Short gap between symbols
                elif symbol == "-":
                    winsound.Beep(frequency, dash_duration)
                    time.sleep(dot_duration / 1000)
                elif symbol == " ":
                    time.sleep((3 * dot_duration) / 1000)  # Gap between letters
                elif symbol == "/":
                    time.sleep((7 * dot_duration) / 1000)  # Gap between words
        except Exception as e:
            logger.error(f"Morse code playback error: {e}")
