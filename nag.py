import sys
from typing import NoReturn
from reporter import Reporter
from typing import List
from stmt import Stmt


class Nag:
    def __init__(self) -> None:
        self.reporter = Reporter()

    def main(self) -> NoReturn:
        args = sys.argv
        print(args)
        if len(args) == 1:
            # repl
            self.run_prompt()
        elif len(args) == 2:
            # run script
            self.run_script(args[1])
        else:
            print("Usage: nag [script].ng")
            exit(64)

    def run_prompt(self) -> NoReturn:
        print("run prompt")
        while True:
            print(">>", end=" ")
            inp = input()
            if inp.strip() == "exit":
                break
            self.run(inp)
            self.reporter.reset()

    def run_script(self, file: str) -> None:
        print("run script for ", file)
        with open(file, "r") as f:
            inp = f.read()
        self.run(inp)
        if self.reporter.had_error:
            exit(65)
        if self.reporter.had_runtime_error:
            exit(70)

    def run(self, source: str) -> None:
        from scanner import Scanner
        from parser import Parser
        from interpreter import Interpreter

        scanner = Scanner(source, self.reporter)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token, sep="\t")
        print()

        if self.reporter.had_error:
            # initiate parser only if lexing worked
            return
        print("l55 starting parser...")
        parser = Parser(tokens, self.reporter)
        statements: List[Stmt] = parser.parse()

        if self.reporter.had_error:
            # initiate interpreter only if parsing worked
            return
        print("l64 starting interpreter...")
        interpreter = Interpreter(self.reporter)
        interpreter.interpret(statements)


if __name__ == "__main__":
    nag = Nag()
    nag.main()
