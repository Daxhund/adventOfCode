from typing import List, Tuple


class Map:
    PADDING_CHAR: str = "%"
    PADDING_SIZE: int = 1

    def __init__(self, raw_map: List[str]) -> None:
        self.map: List[str] = self.__load_map(raw_map)

    def __load_map(self, raw_map: List[str]) -> List[str]:
        map: List[str] = []

        map.append(list(self.PADDING_CHAR * (len(raw_map) + self.PADDING_SIZE * 2 - 1)))
        # Add padding 1 on each side using %
        for line in raw_map:
            map.append(list(self.PADDING_CHAR + line.strip() + self.PADDING_CHAR))
        map.append(list(self.PADDING_CHAR * (len(raw_map) + self.PADDING_SIZE * 2 - 1)))
        return map

    def plot(self) -> None:
        for line in self.map[self.PADDING_SIZE : self.PADDING_SIZE * -1]:
            print(line[self.PADDING_SIZE : self.PADDING_SIZE * -1])

    def __to_padded(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        return (coordinates[0] + self.PADDING_SIZE, coordinates[1] + self.PADDING_SIZE)

    def __from_padded(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        return (coordinates[0] - self.PADDING_SIZE, coordinates[1] - self.PADDING_SIZE)

    def find(self, symbol: str) -> List[Tuple[int, int]]:
        assert len(symbol) == 1  # only looking for chars
        coordinates: List[Tuple[int, int]] = []
        for offset, line in enumerate(self.map):
            coordinates.extend(
                [(offset, x) for x, value in enumerate(line) if value == symbol]
            )
        return [self.__from_padded(cords) for cords in coordinates]

    def get(self, coordinates: Tuple[int, int]) -> str:
        y, x = self.__to_padded(coordinates)
        try:
            return self.map[y][x]
        except IndexError as e:
            raise OutOfMap(e) from e

    def set(self, coordinates: Tuple[int, int], value: str) -> bool:
        assert len(value) == 1
        y, x = self.__to_padded(coordinates)
        try:
            self.map[y][x] = value
            return True
        except IndexError as e:
            raise OutOfMap(e) from e

    def get_start(self) -> Tuple[int, int]:
        return self.find("^")[0]


class Guard:

    def __init__(self, map: Map, location: Tuple[int, int]):
        # (-1,0) top, (0, 1) right,  (1,0) down, (0,-1) left,
        self.directions: List[Tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.orientation: int = 0
        self.map = map
        self.fields_visited: int = 0

        # check if location is valid
        self.location: Tuple[int, int] = self.__validate_start_location(location)

    def __validate_start_location(self, location) -> Tuple[int, int]:
        try:
            self.map.get(location)
        except OutOfMap as e:
            raise Exception("Start location is out of map!") from e

        return location

    def move(self) -> str:
        new_value: str = ""
        for offset in range(4):
            move_instruction = self.directions[(self.orientation + offset) % 4]
            self.orientation = (self.orientation + offset) % 4

            new_coordinates: Tuple[int, int] = (
                self.location[0] + move_instruction[0],
                self.location[1] + move_instruction[1],
            )
            new_value = self.map.get(new_coordinates)
            if new_value != "#":
                self.location = new_coordinates
                break

        if new_value != "+":
            self.map.set(self.location, "+")
            self.fields_visited += 1

        return new_value


def test() -> None:
    with open("src/2024/06/input2.txt") as fh:
        data = fh.readlines()
    map = Map(data)
    guard = Guard(map, map.get_start())
    map.plot()
    new_location = ""
    while new_location != map.PADDING_CHAR:
        new_location = guard.move()
        #map.plot()
        #print("")
    print(guard.fields_visited-1)


if __name__ == "__main__":
    test()


class OutOfMap(Exception):
    pass


class Border(Exception):
    pass
