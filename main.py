# -*- encoding: utf-8 -*-
from sys import argv

from compiler import Parser, PrePro
from compiler.nasm import Nasm
from utils import load_file


def main(case):
    processed = PrePro.filter(case)
    resulting_node = Parser.run(processed)
    resulting_node.evaluate()
    Nasm.dump("program.asm")


if __name__ == '__main__':
    filepath = argv[1]
    content = load_file(filepath)
    main(content)
    file_name, file_ext = filepath.split(".")
    Nasm.dump(f'{file_name}.asm')
