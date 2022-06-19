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
    filepath = argv[1]
    file = os.path.basename(filepath)
    content = load_file(filepath)
    
    main(content)

    stderr.write(f"{filepath} {file.split()}")

    parts = file.split(".")

    Nasm.dump(f'{parts[0]}.asm')
