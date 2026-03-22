from typing import Any
from expr import Expr, ExprVisitor, Binary, Grouping, Literal, Unary


# prefix
class ASTPrinter(ExprVisitor):
    def print(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("Group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        result = [f"({name}"]
        for expr in exprs:
            result.append(" ")
            result.append(expr.accept(self))
        result.append(")")
        return "".join(result)


# postfix
class RPNPrinter(ExprVisitor):
    def print(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        # return self.parenthesize(expr.expression)
        return self.parenthesize("Group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        result = ["("]
        for expr in exprs:
            result.append(expr.accept(self))
            result.append(" ")
        result.append(f"{name}")
        result.append(")")
        return "".join(result)
