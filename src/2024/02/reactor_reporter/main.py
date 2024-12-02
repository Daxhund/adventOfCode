from typing import List


class ReportValidator:
    def __init__(self):
        pass

    def __parse(self, report_data: str) -> List[int]:
        report: List[int] = [int(x) for x in report_data.split(" ")]
        return report

    def __validate_report(self, report: List[int], dampener: bool = False) -> bool:
        deltas = [(n - report[i + 1]) for i, n in enumerate(report[:-1])]

        # This lambda checks if the list is increasing or decreasing and
        # also if the delta between adjacent levels is min 1 and max 3.

        all_increasing_check: List[bool] = map(lambda x: x < 0 and abs(x) <= 3, deltas)
        all_decreasing_check: List[bool] = map(lambda x: x > 0 and abs(x) <= 3, deltas)

        is_valid: bool = all(all_increasing_check) or all(all_decreasing_check)

        if dampener and is_valid is False:
            # I know its dump - but im tired.
            for i in range(len(report)):
                report_modified: List[int] = report.copy()
                report_modified.pop(i)
                is_valid = self.__validate_report(report_modified)
                if is_valid:
                    break

        return is_valid

    def validate_report(self, report_data: str, dampener: bool = True) -> bool:
        report = self.__parse(report_data)
        return self.__validate_report(report, dampener=dampener)


if __name__ == "__main__":
    with open("src/2024/02/reactor_reporter/input2.txt", encoding="utf-8") as fh:
        data: List[str] = fh.readlines()
    validator = ReportValidator()
    # enable part two
    dampener: bool = True
    count_valid: int = sum([validator.validate_report(i, dampener) for i in data])
    print(f"valid reports: {count_valid}")
