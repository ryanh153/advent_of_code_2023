from dataclasses import dataclass
from typing import Self, Union

import numpy as np


def is_digit(char: str) -> bool:
    return char in '0123456789'


def is_symbol(char: str) -> bool:
    return char not in '.0123456789'


@dataclass(frozen=True)
class RowCol:
    row: int
    col: int


@dataclass(frozen=True)
class SchematicNumber:
    start: RowCol
    span: int
    value: int

    @property
    def end(self) -> RowCol:
        return RowCol(self.start.row, self.start.col + self.span)

    def contains(self, pos: RowCol) -> bool:
        if pos.row != self.start.row:
            return False
        return self.start.col <= pos.col < self.start.col + self.span


@dataclass
class Entry:
    pos: RowCol
    value: str


@dataclass
class Gear:
    pos: RowCol
    first_part: int
    second_part: int

    @property
    def ratio(self) -> int:
        return self.first_part * self.second_part


@dataclass
class Schematic:
    grid: np.ndarray[str]

    def __post_init__(self):
        self.entries = [
            Entry(RowCol(row, col), value)
            for row, row_data in enumerate(self.grid)
            for col, value in enumerate(row_data)
        ]

    @classmethod
    def from_file(cls, file: str) -> Self:
        text = [line.strip() for line in open(file, 'r').readlines()]
        return cls(grid=np.array([[char for char in row] for row in text], dtype=str))

    def get_contained_numbers(self) -> list[SchematicNumber]:
        part_numbers = list()
        # This is the grosses part. Should just have detect digit -> walk right to not digit or end -> append -> go from there
        for row_idx, row in enumerate(self.grid):
            start = None
            for col_idx, char in enumerate(row):
                # Path for if we aren't making a part number currently
                if start is None:
                    if not is_digit(char):
                        continue
                    start = col_idx
                    # If we are at the end of a row
                    if self.end_of_row(col_idx):
                        part_numbers.append(SchematicNumber(start=RowCol(row_idx, start), span=1, value=int(char)))

                # Path for if we are making a part number currently
                else:
                    if is_digit(char):
                        if not self.end_of_row(col_idx):
                            continue
                        if col_idx == self.grid.shape[1] - 1:
                            part_numbers.append(SchematicNumber(start=RowCol(row_idx, start),
                                                                span=col_idx - start + 1,
                                                                value=int(
                                                                    ''.join(self.grid[row_idx, start:col_idx + 1]))))
                    else:
                        part_numbers.append(SchematicNumber(start=RowCol(row_idx, start),
                                                            span=col_idx - start,
                                                            value=int(''.join(self.grid[row_idx, start:col_idx]))))
                        start = None
        return part_numbers

    def end_of_row(self, col_idx: int) -> bool:
        return col_idx == self.grid.shape[1] - 1

    def is_part_number(self, number: SchematicNumber) -> bool:
        for col_idx in range(number.start.col, number.end.col):
            if self.any_surrounding_symbols(RowCol(number.start.row, col_idx)):
                return True
        return False

    def any_surrounding_symbols(self, pos: RowCol) -> bool:
        return any(is_symbol(char) for char in self.surrounding_characters(pos))

    def surrounding_positions(self, pos):
        steps = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        steps = [RowCol(*step) for step in steps]
        positions = [RowCol(pos.row + step.row, pos.col + step.col) for step in steps]
        return [pos for pos in positions if not self.out_of_bounds(pos)]

    def surrounding_characters(self, pos: RowCol) -> list[str]:
        return [self.grid[dest.row, dest.col] for dest in self.surrounding_positions(pos)]

    def out_of_bounds(self, pos: RowCol) -> bool:
        return any([pos.row < 0, pos.row >= self.grid.shape[0], pos.col < 0, pos.col >= self.grid.shape[1]])

    def get_gear(self, entry: Entry, parts: dict[RowCol, SchematicNumber]) -> Union[None, Gear]:
        if entry.value != '*':
            return None

        gear_parts = list()
        for dest in self.surrounding_positions(entry.pos):
            part = parts.get(dest, None)
            if part is not None and part not in gear_parts:
                gear_parts.append(part)

        if len(gear_parts) != 2:
            return None
        return Gear(pos=entry.pos, first_part=gear_parts[0].value, second_part=gear_parts[1].value)


def get_part_positions(schematic: Schematic) -> dict[RowCol, SchematicNumber]:
    part_numbers = [number for number in schematic.get_contained_numbers() if schematic.is_part_number(number)]
    return {RowCol(part.start.row, part.start.col + offset): part
            for part in part_numbers for offset in range(part.span)}


def part_one(file: str):
    schematic = Schematic.from_file(file)
    part_numbers = [number for number in schematic.get_contained_numbers() if schematic.is_part_number(number)]
    return sum(part_number.value for part_number in part_numbers)


def part_two(file: str):
    schematic = Schematic.from_file(file)
    part_positions = get_part_positions(schematic)
    gears = [schematic.get_gear(entry, part_positions) for entry in schematic.entries]
    gears = list(filter(lambda x: x is not None, gears))
    return sum(gear.ratio for gear in gears if gear is not None)


def main() -> None:
    input_type = 'real'
    print(f'First: {part_one(f'first_{input_type}_input.txt')}')
    print(f'Second: {part_two(f'first_{input_type}_input.txt')}')


if __name__ == '__main__':
    main()
