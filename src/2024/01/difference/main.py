import re
from typing import List


if __name__ == "__main__":
    with open("src/2024/01/input2.txt", encoding="utf-8") as fh:
        data: List[str] = fh.readlines()
    a_values: List[int] = []
    b_values: List[int] = []
    
    for line in data:
        matches: List[re.Match] = list(re.finditer(r"(\d+)", line))
        a = int(matches[0].group())
        b = int(matches[1].group())
        a_values.append(a)
        b_values.append(b)
    
    a_values.sort()
    b_values.sort()
    
    assert len(a_values) == len(b_values)

    diff_values: List[int] = []
    for i, v in enumerate(a_values):
        diff_values.append(abs(v - b_values[i]))

    print(sum(diff_values))
