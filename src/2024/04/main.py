from typing import Dict, List, Optional, Tuple
from loguru import logger
import re


class Puzzle:
    PADDING_SIZE: int = 3

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
        for i in range(self.PADDING_SIZE):
            matrix.insert(0, list("." * len(matrix[0])))
            matrix.append(list("." * len(matrix[0])))
        return matrix

    def __pad_row(self, line: List[str]) -> List[str]:
        for i in range(self.PADDING_SIZE):
            line.insert(0, ".")
            line.append(".")
        return line

    def get_element(self, i: int, j: int) -> str:
        # +n due to the padding
        return self.matrix[i + self.PADDING_SIZE][j + self.PADDING_SIZE]

    def get_rows(self) -> List[List[str]]:
        matrix: List[List[str]] = []
        # without padding
        for row in self.matrix[self.PADDING_SIZE : self.PADDING_SIZE * -1]:
            matrix.append(row[self.PADDING_SIZE : self.PADDING_SIZE * -1])
        return matrix

    def get_row(self, i: int) -> List[str]:
        return self.matrix[i + self.PADDING_SIZE][
            self.PADDING_SIZE : self.PADDING_SIZE * -1
        ]

    def get_dimensions(self) -> Tuple[int, int]:
        return (
            len(self.matrix) - self.PADDING_SIZE * 2,
            len(self.matrix[0]) - self.PADDING_SIZE * 2,
        )

    def get_adjacent_values(
        self, i: int, j: int, length_word: int = 4, diagonal_only: bool = False
    ) -> List[str]:
        # assert length_word <= self.PADDING_SIZE  # lazy check

        adjacent_words: List[List[str]] = []
        # +n due to the padding
        i_center = i + self.PADDING_SIZE
        j_center = j + self.PADDING_SIZE

        top: List[str] = []
        bottom: List[str] = []
        left: List[str] = []
        right: List[str] = []

        top_left: List[str] = []
        top_right: List[str] = []
        bottom_left: List[str] = []
        bottom_right: List[str] = []

        for i in range(length_word):
            if not diagonal_only:
                top.append(self.matrix[i_center + (i * -1)][j_center])
                bottom.append(self.matrix[i_center + (i)][j_center])
                left.append(self.matrix[i_center][j_center + (i * -1)])
                right.append(self.matrix[i_center][j_center + i])

            top_left.append(self.matrix[i_center + (i * -1)][j_center + (i * -1)])
            top_right.append(self.matrix[i_center + (i * -1)][j_center + (i)])
            bottom_left.append(self.matrix[i_center + (i)][j_center + (i * -1)])
            bottom_right.append(self.matrix[i_center + (i)][j_center + (i)])

        adjacent_words = [
            top_left,
            top,
            top_right,
            left,
            right,
            bottom_left,
            bottom,
            bottom_right,
        ]
        return ["".join(word) for word in adjacent_words if word]

    def count_xmas(self) -> int:
        counter: int = 0
        width, height = self.get_dimensions()
        for x in range(width):
            for y in range(height):
                element = self.get_element(x, y)
                if element == "X":
                    # print(f"({x},{y})")
                    counter += sum(
                        bool(x) for x in self.get_adjacent_values(x, y) if x == "XMAS"
                    )
        return counter

    def count_x_mas(self) -> int:
        counter: int = 0
        width, height = self.get_dimensions()
        for x in range(width):
            for y in range(height):
                element = self.get_element(x, y)
                if element == "A":
                    # print(f"({x},{y})")
                    fragments = [
                        word[-1]
                        for word in self.get_adjacent_values(
                            x, y, length_word=2, diagonal_only=True
                        )
                    ]
                    if (
                        ord(fragments[0]) + ord(fragments[3]) == 160
                        and ord(fragments[1]) + ord(fragments[2]) == 160
                    ):
                        # print(f"{fragments[0]}-{fragments[1]}")
                        # print(f"{fragments[2]}-{fragments[3]}")
                        # print("####")
                        counter += 1
        return counter

    def plot(self) -> None:
        for line in self.matrix:
            print(line)


def test() -> None:
    with open("src/2024/04/input2.txt") as fh:
        data = fh.readlines()
        puzzle = Puzzle(raw_data=data)

        # puzzle.plot()
        print(f"XMAS count: {puzzle.count_xmas()}")
        print(f"X-MAS count: {puzzle.count_x_mas()}")


if __name__ == "__main__":
    test()
