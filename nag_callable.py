from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import time
if TYPE_CHECKING:
    from interpreter import Interpreter

class NagCallable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: List[Any]) -> Any:
        pass
    
    @abstractmethod
    def arity(self) -> int:
        pass

class Clock(NagCallable):
    def call(self, interpreter: Interpreter, arguments: List[Any]) -> float:
        return float(time.time())

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native_fn>"

    def __repr__(self) -> str:
        return f"NagFunction(name = {self.name}, arity = {self.arity()})"
