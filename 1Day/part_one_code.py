import re
from dataclasses import dataclass
from functools import total_ordering
from itertools import dropwhile
from typing import Self, Union, Any

DIGIT_MAP = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
                 'nine': '9'}
REVERSE_DIGIT_MAP = {key[::-1]: value for key, value in DIGIT_MAP.items()}


@total_ordering
@dataclass(frozen=True)
class NumMatch:
    position: int
    value: str

    def __lt__(self, other: Self) -> bool:
        return (self.position, self.value) < (other.position, other.value)


def not_int(char: str) -> bool:
    try:
        int(char)
        return False
    except ValueError:
        return True


def get_first_int_char(chars: str) -> str:
    return next(dropwhile(not_int, chars))


def parse_line_digits_only(line: str) -> int:
    return int(get_first_int_char(line) + get_first_int_char(line[::-1]))


def part_one(file: str) -> int:
    input_txt = [line.strip() for line in open(file, 'r').readlines()]
    result = sum(parse_line_digits_only(line) for line in input_txt)
    return result


def get_num_char_result(line: str) -> Union[None, NumMatch]:
    filtered_line = list(dropwhile(not_int, line))
    if not filtered_line:
        return None
    return NumMatch(position=len(line) - len(filtered_line), value=filtered_line[0])


def add_if_not_none(base: set, result: Union[None, Any]):
    if result is not None:
        base.add(result)


def get_match_result_regex(line: str, pattern: str, value: str) -> Union[None, NumMatch]:
    match = re.search(pattern, line)
    if match is not None:
        return NumMatch(position=match.span()[0], value=value)
    return None


def get_first_int_loose(line: str, match_map: dict[str, str]) -> str:
    matches = set()
    add_if_not_none(matches, get_num_char_result(line))
    for search_for, sub_in in match_map.items():
        add_if_not_none(matches, get_match_result_regex(line, search_for, sub_in))
    return min(matches).value


def parse_line_digits_and_strings(line) -> int:
    return int(get_first_int_loose(line, DIGIT_MAP) + get_first_int_loose(line[::-1], REVERSE_DIGIT_MAP))


def num_str_to_char(line: str) -> str:
    for key, value in DIGIT_MAP.items():
        line = line.replace(key, value)
    return line


def part_two(file: str) -> int:
    input_txt = [line.strip() for line in open(file, 'r').readlines()]
    result = sum(parse_line_digits_and_strings(line) for line in input_txt)
    return result


def main():
    input_type = 'real'
    first_answer = part_one(f'{input_type}_first_input.txt')
    second_answer = part_two(f'{input_type}_second_input.txt')

    print(f'First: {first_answer}\nSecond: {second_answer}')


if __name__ == '__main__':
    main()
