# -*- encoding: utf-8 -*-
from sys import argv

from compiler import Parser, PrePro
from compiler.nasm import Nasm
from utils import load_file


def main(case):
    processed = PrePro.filter(case)
    resulting_node = Parser.run(processed)
    resulting_node.evaluate()


if __name__ == '__main__':
    filepath = argv[1]
    content = load_file(filepath)
    main(content)
    Nasm.dump(f'{filepath}.asm')
