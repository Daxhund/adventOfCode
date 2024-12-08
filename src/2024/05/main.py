from typing import List, Tuple
import re
import math
from dataclasses import dataclass


@dataclass
class Rule:
    a: int
    b: int

    def __str__(self) -> str:
        return f"{self.a} < {self.b}"

    def __repr__(self):
        self.__str__()


class Manual:
    def __init__(self, pages: List[int]):
        self.pages: List[int] = pages

    def get_indexes_by_page_id(self, page_id: int) -> List[int]:
        return [id for id, value in enumerate(self.pages) if value == page_id]

    def get_middle_value(self) -> int:
        offset: int = math.ceil(len(self.pages) / 2) -1
        return self.pages[offset]

    def __str__(self):
        return ",".join([str(x) for x in self.pages])

    def __repr__(self):
        return self.__str__()


class ManualValidator:
    def __init__(self, data: List[str]) -> None:
        self.rulset: List[Rule] = self.extract_rules(data)
        self.manuals: List[Manual] = self.extract_manuals(data)
        self.invalid_manuals: List[Manual] = []

    def __validate_manual(self, manual: Manual) -> int:
        is_valid: bool = True
        for rule in self.rulset:
            before: List[int] = manual.get_indexes_by_page_id(rule.a)
            after: List[int] = manual.get_indexes_by_page_id(rule.b)
            #print(f"rule{rule} on {manual}")
            before = sorted(before)
            after = sorted(after)
            #print(f"before{before}")
            #print(f"after{after}")
            if not (before and after):
                #print("missing index")
                continue

            if before[0] > after[0]:
                is_valid = False
                #print(f"Manual {manual} is invalid due to {rule}")
                self.invalid_manuals.append(manual)
                break
        middle_value: int = 0
        if is_valid is True:
            middle_value = manual.get_middle_value()
            #print(f"Manual {manual} is valid and middle value is {middle_value}")

        return middle_value

    def validate_manuals(self) -> str:
        magic_number: int = 0
        for manual in self.manuals:
            magic_number += self.__validate_manual(manual)
        return f"magic_number of valid manuals: {magic_number}"

    def extract_rules(self, raw_config: List[str]) -> List[Rule]:
        raw_rules: List[Rule] = []
        pattern = r"(\d{1,3})\|(\d{1,3})"
        for line in raw_config:
            if match := re.match(pattern, line):
                raw_rules.append(Rule(int(match.groups()[0]), int(match.groups()[1])))

        return raw_rules

    def extract_manuals(self, data: List[str]) -> List[Manual]:
        manuals: List[Manual] = []
        for line in data:
            if "," in line:
                pages = [int(line) for line in line.split(",")]
                manuals.append(Manual(pages))
        return manuals
    
    def __fix_manual(self, manual:Manual) -> int:
        print(manual)
        return 0




    def sanitize_invalid_manuals(self) -> str:
        magic_number: int = 0
        for manual in self.invalid_manuals.copy():
            magic_number += self.__fix_manual(manual)
        return f"magic_number of **invalid** manuals: {magic_number}"


def test() -> None:
    with open("src/2024/05/input2.txt") as fh:
        data = fh.readlines()
        mv = ManualValidator(data)
        print(mv.validate_manuals())
        #mv.sanitize_invalid_manuals()


if __name__ == "__main__":
    test()
