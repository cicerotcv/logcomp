# -*- encoding: utf-8 -*-
import os
from sys import argv, stderr

from compiler import Parser, PrePro
from compiler.nasm import Nasm
from utils import load_file


def main(case):
    processed = PrePro.filter(case)
    resulting_node = Parser.run(processed)
    resulting_node.evaluate()


if __name__ == '__main__':
    input_path = argv[1]
    content = load_file(input_path)

    main(content)

    # trocar a extensão
    root, ext = os.path.splitext(input_path)

    Nasm.dump(f'{root}.asm')
