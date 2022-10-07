import time
from threading import Thread
from queue import Queue
from enum import Enum

class Part(Enum):
    DETAIL_A = 'DETAIL_A'
    DETAIL_B = 'DETAIL_B'
    DETAIL_C = 'DETAIL_C'
    WIDGET = 'WIDGET'


BOX_A = Queue()
BOX_B = Queue()
BOX_C = Queue()


def bench_basic(part: Part, box: Queue, time_: float):
    while True:
        time.sleep(time_)
        box.put(part)
        print(f'{part.name} created. In Box: {box.qsize()}')


def bench_widget():
    widget_counter = 0
    while True:
        time.sleep(1)
        BOX_A.get()
        BOX_B.get()
        BOX_C.get()
        widget_counter += 1
        print(f'-> {widget_counter} widgets created <-')


def main():
    threads = [
        # INFO: A Benches
        Thread(target=bench_basic, args=(Part.DETAIL_A, BOX_A, 1.0)),
        # INFO: B Benches
        Thread(target=bench_basic, args=(Part.DETAIL_B, BOX_B, 2.0)),
        Thread(target=bench_basic, args=(Part.DETAIL_B, BOX_B, 2.0)),
        # INFO: C Benches
        Thread(target=bench_basic, args=(Part.DETAIL_C, BOX_C, 3.0)),
        Thread(target=bench_basic, args=(Part.DETAIL_C, BOX_C, 3.0)),
        Thread(target=bench_basic, args=(Part.DETAIL_C, BOX_C, 3.0)),
        # INFO: Widget Benches
        Thread(target=bench_widget),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()