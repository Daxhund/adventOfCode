from typing import Dict, List


class One:
    def __init__(self):
        pass

    def __solve_line(self, input: str) -> int:
        numbers_only: List = []
        for i in input:
            if i.isdecimal():
                numbers_only.append(i)
        two_digit = int(numbers_only[0] + numbers_only[-1])
        return two_digit

    def solve(self, input: List[str]) -> int:
        sum_results: int = 0
        for sample in input:
            sum_results += self.__solve_line(sample)
        return sum_results


def test():
    input = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchetc"]
    print(One().solve(input))


if __name__ == "__main__":
    test()
