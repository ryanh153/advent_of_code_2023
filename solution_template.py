from time import perf_counter


def part_one(file: str):
    pass


def part_two(file: str):
    pass


def main() -> None:
    input_type = 'sample'
    start = perf_counter()
    print(f'First: {part_one(f'first_{input_type}_input.txt')}')
    print(f'Second: {part_two(f'first_{input_type}_input.txt')}')
    print(f'Run time {(perf_counter() - start) * 1e3:,.2} ms')


if __name__ == '__main__':
    main()