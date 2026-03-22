from error import InterpreterError


class Reporter:
    def __init__(self) -> None:
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def runtime_error(self, error: InterpreterError) -> None:
        print(
            f"[{error.token.line}] RuntimeError {error.token.lexeme}: {error.message}"
        )
        self.had_runtime_error = True

    def report(self, line: int, location: str, message: str) -> None:
        print(f"[{line}] Error {location}: {message}")
        self.had_error = True

    def reset(self) -> None:
        self.had_error = False
