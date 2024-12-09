import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class Multiplication:
    a: int
    b: int

    def result(self) -> int:
        return self.a * self.b

    @staticmethod
    def from_tuple(values: Tuple[str, str]) -> Any:
        return Multiplication(a=int(values[0]), b=int(values[1]))


class Parser:
    pattern_multiplication: str = r"mul\((\d{1,3}),(\d{1,3})\)"

    def __init__(self):
        pass

    def __parse_multiplication(self, fragment: str) -> List[Multiplication]:
        matches = re.findall(self.pattern_multiplication, fragment)
        operations: List[Multiplication] = [
            Multiplication(int(x[0]), int(x[1])) for x in matches
        ]
        return operations

    def parse(self, code_fragment: str) -> int:
        return sum([op.result() for op in self.__parse_multiplication(code_fragment)])


class Lexer(Parser):
    """This class can build an AST like structure to parse the code fragment"""

    def __init__(self, fragment: str) -> None:
        self.fragment = fragment
        self.instructions = self._parse(self.fragment)

    def parse(self):
        return self.instructions

    def calculate_magic_value(self) -> int:
        return sum(i.result() for i in self.instructions)

    def _parse(self, fragment: str) -> List[Multiplication]:
        tokens: List[Multiplication] = []
        buffer = fragment
        toggle: bool = True
        while len(buffer) > 0:
            if buffer.startswith("do()"):
                toggle = True
                buffer = buffer.lstrip("do()")
            elif buffer.startswith("don't()"):
                toggle = False
                buffer = buffer.lstrip("don't()")
            elif match := re.match(self.pattern_multiplication, buffer):
                if toggle:
                    tokens.append(Multiplication.from_tuple(match.groups()))
                buffer = buffer[match.end() :]

            else:
                buffer = buffer[1:]
        return tokens

    # def _parse(self, fragment: str):
    #     program: str = ""
    #     print(len(fragment))
    #     if len(fragment) > 0:
    #         if fragment.startswith("do()"):
    #             # program.append("do")
    #             print("do!")
    #             program += "do() "
    #             program += self._parse(fragment[4:])

    #         elif fragment.startswith("don't()"):
    #             # program.append("dont")
    #             print("don't!")
    #             program += "dont() "
    #             program += self._parse(fragment[7:])

    #         # if fragment.startswith("mul("):
    #         #     print("mul!")
    #         #     self._parse(fragment[3:])

    #         else:
    #             self._parse(fragment[1:])
    #     else:
    #         return program


if __name__ == "__main__":
    with open("src/2024/03/input2.txt", encoding="utf-8") as fh:
        data: str = fh.read()
    # print(data)
    # print(Parser().parse(data))

    print(Lexer(fragment=data).calculate_magic_value())
