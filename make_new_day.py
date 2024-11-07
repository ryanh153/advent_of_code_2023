import shutil
import sys
from pathlib import Path


def main():
    day = int(sys.argv[1])
    assert 1 <= day <= 25

    solution_template = Path('solution_template.py')
    assert solution_template.exists()

    folder = Path(f'{day}Day')
    folder.mkdir(exist_ok=False, parents=False)

    input_names = [
        'first_sample_input.txt',
        'first_real_input.txt',
        'second_sample_input.txt',
        'second_real_input.txt',
    ]
    for name in input_names:
        file = folder.joinpath(name)
        f = open(file, 'w')
        f.close()

    shutil.copy(str(solution_template.absolute()), str(folder.joinpath('solution.py').absolute()))



if __name__ == '__main__':
    main()