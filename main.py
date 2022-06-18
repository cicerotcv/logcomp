# -*- encoding: utf-8 -*-
from sys import argv

from compiler import Parser, PrePro
from compiler.symboltable import FuncTable, SymbolTable
from utils import load_file


def main(case):
    processed = PrePro.filter(case)
    root = Parser.run(processed)
    root.evaluate(FuncTable)


if __name__ == '__main__':
    filepath = argv[1]
    content = load_file(filepath)
    main(content)
