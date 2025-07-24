"""
Custom exception classes
"""


class YasminBaseException(Exception):
    """Base exception class"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class HandDetectionError(YasminBaseException):
    """Exception class for hand detection related errors"""

    def __init__(self, message="An error occurred during hand detection"):
        super().__init__(message)


class SignLanguageError(YasminBaseException):
    """Exception class for sign language processing related errors"""

    def __init__(self, message="An error occurred during sign language processing"):
        super().__init__(message)


class HandRecognitionException(YasminBaseException):
    """Exception class for hand recognition related errors"""

    def __init__(self, message="An error occurred during hand recognition"):
        super().__init__(message)


class SignLanguageException(YasminBaseException):
    """Exception class for sign language translation related errors"""

    def __init__(self, message="An error occurred during sign language translation"):
        super().__init__(message)


class MorseException(YasminBaseException):
    """Exception class for Morse code translation related errors"""

    def __init__(self, message="An error occurred during Morse code translation"):
        super().__init__(message)


class CameraException(YasminBaseException):
    """Exception class for camera related errors"""

    def __init__(self, message="An error occurred during camera access"):
        super().__init__(message)


class ConfigurationException(YasminBaseException):
    """Exception class for configuration related errors"""

    def __init__(self, message="An error occurred while processing configuration file"):
        super().__init__(message)


"""
Custom error classes for Sign Language Translator.
"""


class YasminError(Exception):
    """Base YASMIN application error."""

    pass


class CameraError(YasminError):
    """Used for camera related errors."""

    pass


class ProcessingError(YasminError):
    """Used for image processing errors."""

    pass


class TranslationError(YasminError):
    """Used for translation errors."""

    pass
