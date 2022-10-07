import time
from threading import Lock, Thread, Event

SORT_DELAY = 30

class SafeList(list):

    def __init__(self):
        super().__init__()
        self._lock = Lock()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


def interface(safe_list: SafeList, stop_event: Event):
    while True:
        command = input('-> ').strip()
        if command:
            with safe_list:
                safe_list.append(int(command))
        else:
            stop_event.set()
            break
        time.sleep(0.1)


def sort_watcher(safe_list: SafeList, stop_event: Event):
    sort_time = time.time() + SORT_DELAY

    while not stop_event.is_set():
        if time.time() > sort_time:
            with safe_list:
                safe_list.sort()
            sort_time = time.time() + SORT_DELAY
        time.sleep(1)

def main():
    safe_list = SafeList()
    stop_event = Event()

    threads = [
        Thread(target=interface, args=(safe_list, stop_event)),
        Thread(target=sort_watcher, args=(safe_list, stop_event)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f'LIST: {safe_list}')


if __name__ == '__main__':
    main()
