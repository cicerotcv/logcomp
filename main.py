# -*- encoding: utf-8 -*-
from sys import argv

from compiler import Parser, PrePro


def main(case):
    processed = PrePro.filter(case)
    resulting_node = Parser.run(processed)
    result = resulting_node.evaluate()
    return result


if __name__ == '__main__':
    case = argv[1]
    print(main(case))

    # cases = [
    #     '(3 + 2) /5',  # 1
    #     '+--++3',  # 3
    #     '3 - -2/4',  # 3
    #     '4/(1+1)*2',  # 4
    #     '(2*2'  # error
    # ]
    # for case in cases:
    # print(f'case: {case}')
    # print(f'R: {main(case)}\n')
