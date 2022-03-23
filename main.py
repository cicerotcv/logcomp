# -*- encoding: utf-8 -*-
from sys import argv

from compiler import Parser, PrePro
from utils import load_file


def main(case):
    processed = PrePro.filter(case)
    resulting_node = Parser.run(processed)
    result = resulting_node.evaluate()
    return result


if __name__ == '__main__':
    filepath = argv[1]
    content = load_file(filepath)
    print(main(content))
