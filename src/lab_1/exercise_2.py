import random
import time
from typing import List, Sequence
from threading import Thread

Matrix = List[List]

class DotProductThread(Thread):

    def __init__(self, row: Sequence[int], column: Sequence[int]):
        super().__init__()
        self._result = None
        self._row = row
        self._column = column

    @property
    def result(self) -> List:
        if self._result is None:
            raise ValueError('Result is not ready')

        return self._result

    def run(self):
        self._result = sum([
            r_value * c_value
            for r_value, c_value in zip(self._row, self._column)
        ])
        # INFO: Just for tests
        time.sleep(random.random())


def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    matrix_n = len(matrix_a)
    matrix_b_transposed = list(zip(*matrix_b))
    if matrix_n != len(matrix_b_transposed):
        raise ValueError('Matrix should be A(m×N) and B(N×k), where N >= 1')

    dot_product_threads = [
        DotProductThread(row, column)
        for row in matrix_a
        for column in matrix_b_transposed
    ]

    for thread in dot_product_threads:
        thread.start()

    dot_product_results = []
    for thread in dot_product_threads:
        thread.join()
        dot_product_results.append(thread.result)

    return [
        dot_product_results[i:i+matrix_n]
        for i in range(0, len(dot_product_results), matrix_n)
    ]


def main():
    matrix_a = [
        [6, 9, 6, 9, 6, 9, 6, 9, 6],
        [9, 6, 9, 6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9, 6, 9, 6],
        [9, 6, 9, 6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9, 6, 9, 6],
        [9, 6, 9, 6, 9, 6, 9, 6, 9],
    ]
    matrix_b = [
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
        [6, 9, 6, 9, 6, 9],
    ]
    print(matrix_multiply(matrix_a, matrix_b))


if __name__ == '__main__':
    main()
