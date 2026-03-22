from typing import Any
from tokentype import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        # override
        return f"{self.type.name} {self.lexeme} {self.literal}"

    def __repr__(self) -> str:
        return self.__str__()
