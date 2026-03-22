from tokenclass import Token, TokenType
from expr import *
from astprinter import ASTPrinter, RPNPrinter

# Let's manually build: -123 * (45.67)
expression = Binary(
    Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)

printer = ASTPrinter()
print(printer.print(expression))


rpnprinter = RPNPrinter()
print(rpnprinter.print(expression))