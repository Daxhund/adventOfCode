import re
from typing import Dict, List, Optional, Tuple

from loguru import logger


class Schematics:
    def __init__(self, raw_data: List[str]):
        self.matrix = self.load_matrix(raw_data)

    def load_matrix(self, data: List[str]) -> List[List[str]]:
        matrix = []
        for line in data:
            line_chars: List[str] = list(line)
            line_chars.pop(-1)  # remove the new line at the end of a line
            line_chars = self.__pad_row(line_chars)
            matrix.append(line_chars)
        matrix = self._pad_top_bottom(matrix)
        return matrix

    def _pad_top_bottom(self, matrix: List[List[str]]) -> List[List[str]]:
        matrix.insert(0, list("." * len(matrix[0])))
        matrix.append(list("." * len(matrix[0])))
        return matrix

    def __pad_row(self, line: List[str]) -> List[str]:
        line.insert(0, ".")
        line.append(".")
        return line

    def get_element(self, i: int, j: int) -> str:
        # +1 due to the padding
        return self.matrix[i + 1][j + 1]

    def get_rows(self) -> List[List[str]]:
        matrix: List[List[str]] = []
        # without padding
        for row in self.matrix[1:-1]:
            matrix.append(row[1:-1])
        return matrix

    def get_row(self, i: int) -> List[str]:
        return self.matrix[i + 1][1:-1]

    def get_dimensions(self) -> Tuple[int, int]:
        return (len(self.matrix) - 2, len(self.matrix[0]) - 2)

    def get_adjacent_values(self, i: int, j: int) -> List[str]:
        # +1 due to the padding
        i_center = i + 1
        # +1 due to the padding
        j_center = j + 1

        # top
        top = self.matrix[i_center - 1][j_center]
        # bottom
        bottom = self.matrix[i_center + 1][j_center]
        # left
        left = self.matrix[i_center][j_center - 1]
        # right
        right = self.matrix[i_center][j_center + 1]
        # top left
        top_left = self.matrix[i_center - 1][j_center - 1]
        # top right
        top_right = self.matrix[i_center - 1][j_center + 1]
        # bottom left
        bottom_left = self.matrix[i_center + 1][j_center - 1]
        # bottom right
        bottom_right = self.matrix[i_center + 1][j_center + 1]

        return [
            top_left,
            top,
            top_right,
            left,
            right,
            bottom_left,
            bottom,
            bottom_right,
        ]

    def plot(self) -> None:
        for line in self.matrix:
            print(line)


class Partnumbers:
    def __init__(self, schematics: Schematics):
        self.schematics = schematics

    def __partnumbers_from_row(self, row) -> List[Tuple[int, List[int]]]:
        matches = list(re.finditer(r"(\d+)", "".join(row)))
        parts = [self.__get_offsets(m) for m in matches]
        return parts

    def __get_offsets(self, match: re.Match) -> Tuple[int, List[int]]:
        first: int = match.start()
        last: int = match.end()
        offsets: List[int] = list(range(first, last))
        return (int(match.group()), offsets)

    def get_partnumbers(self) -> List[int]:
        part_numbers: List[int] = []
        for row_id, row in enumerate(self.schematics.get_rows()):
            if matches := self.__partnumbers_from_row(row):
                for match in matches:
                    number = match[0]
                    offsets = match[1]
                    for offset in offsets:
                        adjacent: List[str] = self.schematics.get_adjacent_values(
                            row_id, offset
                        )
                        if self.__valid_keys(adjacent):
                            part_numbers.append(number)
                            break

        return part_numbers

    def __valid_keys(self, values: List[str]) -> bool:
        s: str = "".join([i for i in values if not i.isdigit()])
        s = s.replace(".", "")
        return bool(s)


def test() -> None:
    with open("src/aoc/three/schematics2.txt") as fh:
        data = fh.readlines()
        schematics = Schematics(raw_data=data)

        schematics.plot()
        pn = Partnumbers(schematics)
        print(sum(pn.get_partnumbers()))


if __name__ == "__main__":
    test()
