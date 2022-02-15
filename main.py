# -*- encoding: utf-8 -*-
from sys import argv
from typing import List

OPERATIONS = {
    '+': lambda before, after: before + after,
    '-': lambda before, after: before - after
}


def reduce(function, iterable, initial_value):
    if len(iterable) == 0:
        return initial_value
    current_value = function(initial_value, iterable[0])
    return reduce(function, iterable[1:], current_value)


def tokenize(expression: str):
    """Quebra expressões em operadores e números"""
    tokens = []
    start = 0
    length = len(expression)
    for end in range(length):
        if expression[end] in OPERATIONS.keys():
            tokens.append(expression[start:end])
            tokens.append(expression[end])
            start = end + 1
        if end == length - 1:
            tokens.append(expression[start:end+1])
    return tokens


def trim(tokens: List[str]):
    return [token.strip() for token in tokens]


def calculate(tokens: List[str]):
    accumulator = 0
    last_op = '+'
    for token in tokens:
        if token.isalnum():
            token = int(token)
            function = OPERATIONS[last_op]
            accumulator = function(accumulator, int(token))
        elif token in OPERATIONS.keys():
            last_op = token
        else:
            continue
    return accumulator


def pipeline(value, function):
    return function(value)


def main(case):
    rst = reduce(pipeline, [tokenize, trim, calculate], case)
    print(rst)


if __name__ == '__main__':
    case = argv[1]
    main(case)
