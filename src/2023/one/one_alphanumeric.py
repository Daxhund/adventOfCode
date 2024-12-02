from typing import Dict, List
import re


class One:
    def __init__(self, calibration_document: List[str]) -> None:
        self.calibration_document = calibration_document
        self.index: Dict[int, Dict[int, int]] = self.__build_index(
            self.calibration_document
        )

    def __build_index(self, data: List[str]) -> Dict[int, Dict[int, int]]:
        index: Dict[int, Dict[int, int]] = {}
        for i, row in enumerate(data):
            index[i] = self.__build_row_index(row)
        return index

    def __build_row_index(self, row) -> Dict[int, int]:
        row_index: Dict[int, int] = {}
        numeric_index = self.__collect_numeric_offsets(row)
        written_number_index = self.__collect_written_numbers_offsets(row)

        row_index = {**numeric_index, **written_number_index}
        row_index = dict(sorted(row_index.items()))

        return row_index

    def __collect_numeric_offsets(self, row: str) -> int:
        numbers_only_offsets: Dict[int, int] = {}
        for offset, number in enumerate(row):
            if number.isdecimal():
                numbers_only_offsets[offset] = number
        return numbers_only_offsets

    def __collect_written_numbers_offsets(self, row: str) -> Dict[int, int]:
        written_numbers_offsets: Dict[int, int] = {}
        pattern = r"zero|one|two|three|four|five|six|seven|eight|nine"
        mapping: Dict[str, int] = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        matches: List[re.Match] = list(re.finditer(pattern, row))
        written_numbers_offsets = {
            int(match.start()): int(mapping.get(match.group())) for match in matches
        }

        return written_numbers_offsets

    def __calculate_magic_number(self, row_index: Dict[int, int]) -> int:
        first_digit = str(row_index[min(row_index)])
        last_digit = str(row_index[max(row_index)])
        return first_digit + last_digit

    def sum_of_magic_numbers(self) -> int:
        return sum(
            [int(self.__calculate_magic_number(index)) for index in self.index.values()]
        )


if __name__ == "__main__":
    with open("src/2023/one/input.txt", encoding="utf-8") as fh:
        input_data: List[str] = fh.readlines()
    parser = One(calibration_document=input_data)
    print(parser.sum_of_magic_numbers())
