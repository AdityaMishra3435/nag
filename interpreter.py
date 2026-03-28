from expr import (
    Expr,
    ExprVisitor,
    Binary,
    Grouping,
    Literal,
    Unary,
    Variable,
    Assign,
    Logical,
    Call
)
from stmt import Stmt, StmtVisitor, Print, ExprStmt, Var, Block, If, While, Return
from reporter import Reporter
from typing import Any, List
from tokentype import TokenType
from tokenclass import Token
from error import InterpreterError
from environment import Env
from nag_callable import NagCallable, Clock
from nag_function import NagFunction


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, reporter: Reporter) -> None:
        self.reporter = reporter
        self.global_env = Env()
        self.env = self.global_env

        clock_fn = NagCallable
        self.global_env.define("clock", Clock)
        
    def interpret(self, statements: List[Stmt]) -> Any:
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as error:
            self.reporter.runtime_error(error)

    # statement methods
    def visit_expr_stmt(self, stmt: ExprStmt) -> None:
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, stmt: Var) -> None:
        print("l41 stmt = ", stmt)
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    def visit_block_stmt(self, stmt: Block) -> None:
        # pass in a new environment within self.env
        self.execute_block(stmt.statements, Env(self.env))
        return None

    def execute_block(self, statements: List[Stmt], env: Env) -> None:
        previous_env = self.env
        try:
            # use new env
            self.env = env
            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous_env
    
    def visit_if_stmt(self, stmt: If) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: While) -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_function_stmt(self, stmt: Function) -> None:
        function = NagFunction(stmt, self.env)
        self.env.define(stmt.name.lexeme, function)

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)
    # expression methods
    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * float(right)
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise InterpreterError(expr.operator, "Division by zero.")
                return left / float(right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise InterpreterError(
                    expr.operator, "Operands must be two numbers or two strings."
                )

            # comparisons
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right

            # equals
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        if expr.value == "nil":
            return None
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.is_truthy(right)
        return None

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.env.get(expr.name)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)
        # early termination cases
        if expr.operator.type == TokenType.OR and self.is_truthy(left):
            return left
        elif expr.operator.type == TokenType.AND and not self.is_truthy(left):
            return left
        return self.evaluate(expr.right)

    def visit_call_expr(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, NagCallable):
            raise InterpreterError(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity():
            raise InterpreterError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        return callee.call(self, arguments)

    # helper methods
    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise InterpreterError(operator, "Operand must be a number.")

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise InterpreterError(operator, "Operands must be numbers.")

    def is_truthy(self, expr: Any) -> bool:
        if expr is None:
            return False
        if isinstance(expr, bool):
            return expr
        return True

    def is_equal(self, left: Any, right: Any) -> bool:
        # (None==None) is True in python
        return left == right

    # method for expressions
    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    # method for statements
    def execute(self, stmt: Stmt) -> None:
        return stmt.accept(self)

    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float):
            text = str(value)
            # convert float to int, if it represents an int
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)
