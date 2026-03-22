from tokenclass import Token


class ParseError(RuntimeError):
    """Custom exception to unwind the parser stack on syntax errors to synchronize when in panic mode"""

    pass


class InterpreterError(RuntimeError):
    """Custom error for runtime errors thrown while running the interpreter."""

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token
        self.message = message
