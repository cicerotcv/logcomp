# -*- encoding: utf-8 -*-
from sys import argv
from typing import List

OPERATORS = {
    '+': lambda before, after: before + after,
    '-': lambda before, after: before - after
}


def reduce(function, iterable, initial_value):
    """reducer recursivo que aplica a função em cada 
    elemento do iterável e usa o resultado como entrada da próxima iteração"""
    if len(iterable) == 0:
        return initial_value
    current_value = function(initial_value, iterable[0])
    return reduce(function, iterable[1:], current_value)


def clean(expression: str):
    return expression.replace(' ', '')


def tokenize(expression: str):
    """Quebra expressões em operadores e números"""
    tokens = []
    start = 0
    length = len(expression)
    for end in range(length):
        if expression[end] in OPERATORS.keys():
            tokens.append(expression[start:end])
            tokens.append(expression[end])
            start = end + 1
        if end == length - 1:
            tokens.append(expression[start:end+1])
    return tokens


def calculate(tokens: List[str]):
    """Itera sobre a lista de tokens e faz operações entre os números"""
    accumulator = 0
    last_op = '+'
    for token in tokens:
        if token.isnumeric():
            token = int(token)
            function = OPERATORS[last_op]
            accumulator = function(accumulator, int(token))
        elif token in OPERATORS.keys():
            last_op = token
        else:
            continue
    return accumulator


def safe_guard(case: str):
    for char in case:
        if not char.isnumeric() and char not in OPERATORS.keys():
            raise Exception(f"Unrecognized char '{char}'")

    if all([operator not in case for operator in OPERATORS.keys()]):
        raise Exception("No operator found in the expression")

    if case.startswith('+'):
        raise Exception("Expression starts with '+'")

    if case.endswith('+') or case.endswith('-'):
        raise Exception("Expression ends with '-' or '+'")

    return case


def main(case):
    pipeline = [clean, safe_guard, tokenize, calculate]
    rst = reduce(lambda value, f: f(value), pipeline, case)
    print(rst)


if __name__ == '__main__':
    case = argv[1]
    main(case)
