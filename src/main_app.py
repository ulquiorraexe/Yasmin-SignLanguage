"""
Sign Language Translator Main Application Module

This module contains the main components of the sign language translator application.
Processes camera images, translates sign language to text, and offers various translation options.

Features:
    - Real-time sign language detection
    - Text translation (TR-EN, EN-TR)
    - Morse code conversion
    - Keyboard shortcut support
"""

import logging
import threading
import time
import tkinter as tk
from tkinter import messagebox

import cv2

# Import modules
from src.app_state import AppState
from src.exceptions import CameraError, ProcessingError, TranslationError
from src.morse_service import MorseCodeService
from src.sign_language_service import SignLanguageService
from src.translator_service import TranslatorService

logger = logging.getLogger(__name__)


class SignLanguageApp:
    """
    Main class of the sign language translator application.

    This class manages all core functions of the application:
    - Processing camera images
    - Translating sign language to text
    - Text translation
    - Morse code conversion
    - User interface management

    Attributes:
        root (tk.Tk): Main application window
        sign_language_service (SignLanguageService): Sign language processing service
        translation_service (TranslatorService): Text translation service
        application_state (AppState): Application state manager
    """

    def __init__(self, root_window, ui_class):
        """
        Constructor method for SignLanguageApp class.

        Args:
            root_window (tk.Tk): Main application window
            ui_class (class): UI class to use (e.g. AppUI)

        Raises:
            ValueError: If UI class is invalid
            RuntimeError: If camera cannot be started
        """
        # Main window settings
        self.root = root_window
        self.root.title("Sign Language Translator")
        self.root.geometry("1280x720")

        # Keyboard focus
        self.root.focus_set()

        # Services
        self.sign_language_service = SignLanguageService()
        self.translation_service = TranslatorService()
        self.application_state = AppState()

        # Make variables public for UI compatibility
        self.required_stable_frames = self.sign_language_service.required_stable_frames

        # Translation settings
        self.translation_direction = tk.StringVar(value="tr-en")

        # Create UI
        self.ui_class = ui_class
        self.user_interface = self.ui_class(self.root, self)

        # Set up keyboard shortcuts
        self._setup_keyboard_shortcuts()

        logger.info("Sign language translator application started")

    def _setup_keyboard_shortcuts(self):
        """Sets up keyboard shortcuts."""
        self.root.bind("<space>", lambda e: self.add_space())
        self.root.bind("<BackSpace>", lambda e: self.delete_last_letter())
        self.root.bind("<Return>", lambda e: self.translate_text())
        self.root.bind("q", lambda e: self.quit_app())

    def toggle_camera(self):
        """Turns the camera on and off."""
        if self.application_state.get("is_running"):
            self.application_state.set("is_running", False)
            self.user_interface.start_button.configure(text="Start Camera")
            self.user_interface.status_label.configure(text="Stopped")

            if self.application_state.get("cap") is not None:
                self.application_state.get("cap").release()
                self.application_state.set("cap", None)
        else:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return

            self.application_state.set("cap", cap)
            self.application_state.set("is_running", True)
            self.user_interface.start_button.configure(text="Stop Camera")
            self.user_interface.status_label.configure(text="Running...")

            # Start camera stream in a separate thread
            threading.Thread(target=self.process_camera, daemon=True).start()

    def _process_frame(self, camera_frame):
        """
        Processes a single camera frame.

        Args:
            camera_frame (np.ndarray): Camera frame to process

        Returns:
            tuple: Processed frame, detected letter, and stability info
        """
        return self.sign_language_service.process_frame(camera_frame)

    def _update_stability_ui(self, stability_percentage):
        """
        Updates stability indicators.

        Args:
            stability_percentage (float): Stability percentage
        """
        if stability_percentage is not None:
            self.user_interface.stability_label.configure(
                text=f"{int(stability_percentage)}%"
            )
            self.user_interface.progress_var.set(stability_percentage)

    def _handle_prediction(
        self, predicted_letter, prediction_count, is_prediction_stable
    ):
        """
        Handles letter prediction and updates the UI.

        Args:
            predicted_letter (str): Most frequently predicted letter
            prediction_count (int): Number of predictions
            is_prediction_stable (bool): Is the prediction stable
        """
        if predicted_letter and prediction_count > 0:
            # Update progress bar
            progress = min(
                prediction_count, self.sign_language_service.required_stable_frames
            )
            self.user_interface.update_letter_progress(progress)

            # If there is a stable prediction and it has not been added before
            is_new_letter = (
                predicted_letter != self.application_state.get("last_added_letter")
                or self.application_state.get("current_word") == ""
            )

            if is_prediction_stable and is_new_letter:
                # Add the predicted letter
                self.application_state.add_letter(predicted_letter)
                self.user_interface.letter_label.configure(text=predicted_letter)

                # Update text
                self.update_text()

                # Clear prediction list
                self.sign_language_service.clear_predictions()

                # Reset progress bar
                self.user_interface.update_letter_progress(0)

    def _update_camera_display(
        self, processed_frame, current_time, last_update_time, update_interval
    ):
        """
        Updates the camera image in the UI.

        Args:
            processed_frame (np.ndarray): Processed camera frame
            current_time (float): Current time
            last_update_time (float): Last update time
            update_interval (float): Update interval

        Returns:
            float: New last update time
        """
        if current_time - last_update_time >= update_interval:
            if self.application_state.get("is_running"):
                cv2_img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                img = self.convert_to_tk_image(cv2_img)
                self.user_interface.set_camera_image(img)
                self.root.update_idletasks()
                self.root.update()
                return current_time
        return last_update_time

    def process_camera(self):
        """
        Continuously processes the camera image.

        This method runs in a separate thread and does the following:
        1. Captures frames from the camera
        2. Sends the frame to the sign language service
        3. Translates detected signs to text
        4. Updates the UI

        Performance:
            - 30 FPS is targeted
            - Sleep is used to reduce frame processing load

        Raises:
            CameraError: If camera image cannot be obtained
            ProcessingError: If an error occurs during frame processing
        """
        last_update_time = time.time()
        update_interval = 1.0 / 30.0  # 30 FPS

        while (
            self.application_state.get("is_running")
            and self.application_state.get("cap") is not None
        ):
            try:
                ret, frame = self.application_state.get("cap").read()

                if not ret:
                    raise CameraError("Could not get camera image!")

                # Process the frame
                processed_frame, letter, stability_info = self._process_frame(frame)

                # Update stability indicators
                self._update_stability_ui(stability_info)

                # Update letter prediction
                (predicted_letter, _, prediction_count, is_prediction_stable) = (
                    self.sign_language_service.update_prediction(letter)
                )

                # Handle prediction results
                self._handle_prediction(
                    predicted_letter, prediction_count, is_prediction_stable
                )

                # Update camera image
                current_time = time.time()
                last_update_time = self._update_camera_display(
                    processed_frame, current_time, last_update_time, update_interval
                )

            except CameraError as e:
                logger.error("Camera error: %s", str(e))
                break
            except ProcessingError as e:
                logger.error("Processing error: %s", str(e))
            except Exception as e:
                logger.error("Unexpected error: %s", str(e))

            # Performance improvement
            time.sleep(0.01)

        # When loop ends, release camera
        if self.application_state.get("cap") is not None:
            self.application_state.get("cap").release()
            self.application_state.set("cap", None)

    def convert_to_tk_image(self, img):
        """Prepares OpenCV image for Tkinter."""
        img = cv2.resize(img, (640, 480))
        return img  # Only resize, no conversion

    def update_text(self):
        """Updates the text in the UI."""
        self.user_interface.text_label.configure(
            text=self.application_state.get_display_text()
        )

    def add_space(self):
        """Adds a space to the text."""
        logger.debug("Adding space...")

        self.application_state.add_space()

        # UI update
        self.update_text()

        # Keyboard focus
        self.root.focus_set()

        return "break"  # Stop event chain

    def delete_last_letter(self):
        """Deletes the last letter."""
        logger.debug("Deleting last letter...")

        self.application_state.delete_last_letter()

        # UI update
        self.update_text()

        # Keyboard focus
        self.root.focus_set()

        return "break"  # Stop event chain

    def translate_text(self):
        """Translates the text."""
        # First, add the current word
        if self.application_state.get("current_word"):
            self.application_state.add_space()
            self.update_text()

        # If text to translate is not empty
        text_to_translate = self.application_state.get_display_text().strip()

        if text_to_translate:
            try:
                # Split language pair
                lang_pair = self.translation_direction.get().split("-")
                src_lang, dest_lang = lang_pair[0], lang_pair[1]

                # Translate text
                translated_text = self.translation_service.translate(
                    text_to_translate, src_lang, dest_lang
                )

                # Save and display results
                self.application_state.set("translated_text", translated_text)
                self.user_interface.translation_label.configure(text=translated_text)

                # Success message
                success_msg = (
                    "Translation completed. "
                    "If you want, you can convert the translation to Morse code."
                )
                self.user_interface.status_label.configure(text=success_msg)

            except TranslationError as e:
                # Display error messages
                error_msg = f"Translation error: {e}"
                logger.error("Translation error: %s", str(e))
                self.user_interface.translation_label.configure(text=error_msg)
                self.user_interface.status_label.configure(
                    text="Translation error occurred."
                )

    def convert_to_morse(self):
        """Converts text to Morse code."""
        display_text = self.application_state.get_display_text()
        if display_text:
            morse_text = MorseCodeService.text_to_morse(display_text)
            self.user_interface.morse_label.configure(text=morse_text)
        else:
            messagebox.showinfo("Warning", "Text to translate not found!")

    def convert_translation_to_morse(self):
        """Converts translation to Morse code."""
        translated_text = self.application_state.get("translated_text")
        if translated_text:
            morse_text = MorseCodeService.text_to_morse(translated_text)
            self.user_interface.morse_label.configure(text=morse_text)
        else:
            messagebox.showinfo("Warning", "First translate the text!")

    def play_morse(self):
        """Plays Morse code."""
        morse_text = self.user_interface.morse_label.cget("text")

        if morse_text:
            threading.Thread(
                target=MorseCodeService.play_morse_code, args=(morse_text,), daemon=True
            ).start()
        else:
            messagebox.showinfo("Warning", "First translate the text!")

    def clear_text(self):
        """Clears all text."""
        # Clear prediction
        self.sign_language_service.clear_predictions()

        # Clear state
        self.application_state.clear()

        # Clear UI
        self.user_interface.letter_label.configure(text="")
        self.user_interface.text_label.configure(text="")
        self.user_interface.translation_label.configure(text="")
        self.user_interface.morse_label.configure(text="")
        self.user_interface.stability_label.configure(text="0%")
        self.user_interface.status_label.configure(text="Ready")
        self.user_interface.progress_var.set(0)

        # Reset letter processing progress
        if hasattr(self.user_interface, "update_letter_progress"):
            self.user_interface.update_letter_progress(0)

    def quit_app(self):
        """Quits the application."""
        self.application_state.set("is_running", False)

        # Release resources
        if self.application_state.get("cap") is not None:
            self.application_state.get("cap").release()

        self.sign_language_service.release_resources()
        self.root.destroy()
        logger.info("Application closed")
