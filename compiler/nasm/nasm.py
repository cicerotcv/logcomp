

import os


def read_file(path) -> str:
    with open(path, 'r') as header:
        return header.read()

class Queue:
    def __init__(self):
        self._values = []

    def __len__(self):
        return len(self._values)

    @property
    def length(self):
        return len(self)

    @property
    def is_empty(self):
        return self.length == 0

    def add(self, value):
        self._values.append(value)

    def take(self):
        return self._values.pop(0)


class Nasm:
    queue = Queue()

    @staticmethod
    def put(nasm_code):
        Nasm.queue.add(nasm_code)

    @staticmethod
    def dump(output_file: str):
        print(read_file('header.txt'))
        while not Nasm.queue.is_empty:
            print(Nasm.queue.take())
        print(read_file('footer.txt'))
