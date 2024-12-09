import re
from typing import Dict, List


class Similarity:

    def __init__(self, list_a: List[int], list_b: List[int]):
        self.list_a = list_a
        self.list_b = list_b

        self.index_b: Dict[int, List[int]] = self.__build_index(self.list_b)

    def __build_index(self, data: List[int]):
        index: Dict[int, List[int]] = {}
        for offset, element in enumerate(data):
            if index.get(element):
                index[element].append(offset)
            else:
                index[element] = [offset]
        return index

    def calculate_similarity(self) -> int:
        score: List[int] = []
        for element in self.list_a:
            element_score = (
                element * len(self.index_b.get(element))
                if self.index_b.get(element)
                else 0
            )
            score.append(element_score)
        return sum(score)


if __name__ == "__main__":
    with open("src/2024/01/similarity/input2.txt", encoding="utf-8") as fh:
        data: List[str] = fh.readlines()

    a_values: List[int] = []
    b_values: List[int] = []

    for line in data:
        matches: List[re.Match] = list(re.finditer(r"(\d+)", line))
        a = int(matches[0].group())
        b = int(matches[1].group())
        a_values.append(a)
        b_values.append(b)

    sim = Similarity(a_values, b_values)

    sim_score: int = sim.calculate_similarity()

    print(sim_score)
