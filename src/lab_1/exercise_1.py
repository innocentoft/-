import time
from typing import List
from threading import Thread

def thread_print(*strings: List[str]) -> None:
    for string in strings:
        print(string)
        time.sleep(0.1)


def main():
    threads = (
        Thread(
            target=thread_print,
            args=[
                f'Thread_{i}-string_{j}'
                for j in range(1, 5)
            ],
        )
        for i in range(1, 5)
    )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
