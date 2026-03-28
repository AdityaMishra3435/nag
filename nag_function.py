from nag_callable import NagCallable
from stmt import Function, Return
from dataclasses import dataclass
from environment import Env
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from interpreter import Interpreter

@dataclass
class NagFunction(NagCallable):
    declaration: Function
    closure: Env
    
    def call(self, interpreter: Interpreter, arguments: List[Any]) -> None:
        env = Env(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params.get(i).lexeme, arguments.get(i));
        try:
            interpreter.execute_block(self.declaration.body, env)
        except Return as return_statement:
            return return_statement.value
        return None
        
    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def __repr__(self):
        return f"NagFunction(declaration = {self.declaration.name.lexeme}"

