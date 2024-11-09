import operator
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from itertools import accumulate
from typing import Self


class Color(Enum):
    red = 'red'
    green = 'green'
    blue = 'blue'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


@dataclass
class DrawResult:
    cube_counts: dict[Color, int]

    @classmethod
    def from_txt(cls, draw_text: str) -> Self:
        matches = {color: re.search(rf'(\d+) {color}', draw_text) for color in Color}
        assert any(color_match is not None for color_match in matches)

        return cls({
            color: int(match.groups()[0]) if match is not None else 0 for color, match in matches.items()
        })


@dataclass
class Game:
    id: int
    draws: list[DrawResult]

    @classmethod
    def from_txt(cls, text: str) -> Self:
        game_id_match = re.match(r'Game (\d+):', text)
        assert game_id_match is not None

        results = [DrawResult.from_txt(draw_text) for draw_text in text[game_id_match.span()[1] + 1:].split(';')]

        return cls(id=int(game_id_match.groups()[0]), draws=results)

    def possible(self, limits: dict[Color, int]) -> bool:
        for draws in self.draws:
            for color, count in draws.cube_counts.items():
                if count > limits[color]:
                    return False
        return True

    def max_of_color(self, color: Color) -> int:
        return max(draw.cube_counts[color] for draw in self.draws)

    @property
    def power(self) -> int:
        return reduce(operator.mul, (self.max_of_color(color) for color in Color), 1)


def part_one(file: str) -> int:
    games = [Game.from_txt(line.strip()) for line in open(file, 'r').readlines()]
    limits = {Color.red: 12, Color.green: 13, Color.blue: 14}
    return sum(game.id for game in games if game.possible(limits))


def part_two(file: str) -> int:
    games = [Game.from_txt(line.strip()) for line in open(file, 'r').readlines()]
    return sum(game.power for game in games)


def main():
    input_type = 'sample'
    # print(f'First: {part_one(f'first_{input_type}_input.txt')}')
    print(f'Second: {part_two(f'first_{input_type}_input.txt')}')


if __name__ == '__main__':
    main()
