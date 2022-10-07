import os
from functools import reduce
from threading import Thread

OPERATIONS = {
    '+': sum,
    '-': lambda values: reduce(lambda x, y: x - y, values),
    '*': lambda values: reduce(lambda x, y: x * y, values),
    '/': lambda values: reduce(lambda x, y: x / y, values),
}


class FileCalcThread(Thread):

    def __init__(self, file_path: str):
        super().__init__()
        self._result = None
        self._file_path = file_path

    @property
    def result(self) -> float:
        if self._result is None:
            raise ValueError('Result is not ready')
        return self._result

    def run(self):
        with open(self._file_path, mode='r') as file:
            symbol = file.readline().strip()
            values = file.readline().strip()

        self._result = OPERATIONS[symbol]([
            int(value)
            for value in values.split(' ')
        ])


def main(dir_path: str, out_file_path: str):
    dir_path_files = os.listdir(dir_path)

    threads = [
        FileCalcThread(file_path=os.path.join(dir_path, file))
        for file in dir_path_files
    ]

    for thread in threads:
        thread.start()

    results = []
    for thread in threads:
        thread.join()
        results.append(thread.result)

    # print(f'{results=}')
    with open(out_file_path, mode='w') as file:
        file.write(f'{sum(results)}\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Lab 1 - Exercise 3')
    parser.add_argument(
        'dir_path', metavar='DIR', type=str, help='path to the dir with files',
    )
    parser.add_argument(
        'out_path', metavar='OUT', type=str, help='path to the out file',
    )
    args = parser.parse_args()

    main(dir_path=args.dir_path, out_file_path=args.out_path)
