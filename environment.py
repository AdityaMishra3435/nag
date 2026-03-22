from typing import Any
from tokenclass import Token
from error import InterpreterError


class Env:
    def __init__(self, enclosing: Env = None):
        self.values = dict()
        self.enclosing = enclosing

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        # look for variable in outer scope if not found in current scope
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise InterpreterError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        # look for variable to assign to in outer scope if not found in current scope
        if self.enclosing is not None:
            return self.enclosing.assign(name, value)
        raise InterpreterError(name, f"Undefined variable '{name.lexeme}'.")
