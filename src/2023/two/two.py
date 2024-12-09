from typing import Dict, List, Optional

from loguru import logger


class Bag:
    def __init__(self, configuration: Dict[str, int]) -> None:
        self.configuration = configuration
        self.content: Dict[str, int] = configuration

    def print_content(self) -> None:
        print("The bag contains currently:")
        for k, v in self.configuration.items():
            print(f" - {v} cubes in {k}")

    def sum_of_cubes(self) -> int:
        sum_cubes: int = 0
        for count in self.configuration.values():
            sum_cubes += count
        return sum_cubes

    def get_cube_count(self, color: Optional[str]):
        sum_cubes = 0
        if not color:
            sum_cubes = self.sum_of_cubes()
        else:
            sum_cubes = self.content.get(color, 0)

        return sum_cubes


class Two:
    def __init__(self, bag: Bag):
        self.bag = bag

    def is_valid_game(self, game: List[Dict[str, int]]) -> bool:
        for turn in game:
            logger.debug(f"turn: {turn}")
            for color, count in turn.items():
                logger.debug(
                    f"check: {color}:{count} <= {self.bag.get_cube_count(color=color)}"
                )
                assert count >= 0
                if not (count <= self.bag.get_cube_count(color=color)):
                    return False
        return True

    def solve(self, input: List[str]) -> int:
        return 0


def test() -> None:
    games_data: Dict[str, List[Dict[str, int]]] = {
        "1": [
            {"blue": 3, "red": 4},
            {"red": 1, "green": 2, "blue": 6},
            {"green": 2},
        ],
        "2": [
            {"blue": 1, "green": 2},
            {"green": 3, "blue": 4, "red": 1},
            {"green": 1, "blue": 1},
        ],
        "3": [
            {"green": 8, "blue": 6, "red": 20},
            {"blue": 5, "red": 4, "green": 13},
            {"green": 5, "red": 1},
        ],
        "4": [
            {"green": 1, "red": 3, "blue": 6},
            {"green": 3, "red": 6},
            {"green": 3, "blue": 15, "red": 14},
        ],
        "5": [
            {"red": 6, "blue": 1, "green": 3},
            {"blue": 2, "red": 1, "green": 2},
        ],
    }
    bag = Bag(configuration={"red": 12, "green": 13, "blue": 14})
    bag.print_content()

    two = Two(bag=bag)
    print("Check if valid:")
    for game_id, data in games_data.items():
        sum_result = 0
        is_valid = two.is_valid_game(data)
        if is_valid:
            sum_result += int(game_id)
        print(f"- Game {game_id} is valid: {is_valid}")
    print(f"sum of games: {sum_result}")


if __name__ == "__main__":
    test()
