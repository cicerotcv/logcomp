# -*- encoding: utf-8 -*-
from sys import argv

# types
T_INT = 'int'
T_PLUS = 'plus'
T_MINUS = 'minus'
T_EOE = 'end_of_expression'

# errors
E_INITIAL_CHAR = 'initial_char'
E_INVALID_TOKEN = 'invalid_token'


class Error(Exception):
    def __init__(self, code, message):
        super().__init__({'code': code, 'message': message})


class InvalidToken(Error):
    def __init__(self, message) -> None:
        super().__init__("invalid-token", message)


class InvalidExpression(Error):
    def __init__(self, message) -> None:
        super().__init__("invalid-expression", message)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value != None:
            return f'<{self.type}:{self.value}>'
        return f'<{self.type}>'

    def isNumber(self):
        return self.type == T_INT

    def __add__(self, another):
        if self.value != None:
            return Token(T_INT, 10*int(self.value) + int(another.value))


class Tokenizer:
    def __init__(self, origin: str):
        self.origin: str = origin
        self.position: int = 0
        self.current: Token = None

    def selectNext(self):

        # self.current já consumiu o último caractere e self.origin
        if self.position >= len(self.origin):
            self.current = Token(T_EOE)
            return self.current

        # consumir espaços
        while self.origin[self.position] == ' ':
            self.position += 1
            if self.position >= len(self.origin):
                self.current = Token(T_EOE)
                return self.current

        if self.origin[self.position] == '+':
            self.current = Token(T_PLUS)
            self.position += 1
            return self.current

        if self.origin[self.position] == '-':
            self.current = Token(T_MINUS)
            self.position += 1
            return self.current

        if self.origin[self.position].isdigit():
            candidate = ''

            while self.origin[self.position].isdigit():
                candidate += self.origin[self.position]
                self.position += 1
                if self.position >= len(self.origin):
                    break

            self.current = Token(T_INT, int(candidate))
            return self.current

        tokenValue = self.origin[self.position]
        raise Exception(f"Unrecognized token '{tokenValue}'")


class Parser:
    tokens: Tokenizer = None

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        accumulator = tokens.selectNext().value

        while tokens.current.type != T_EOE:
            currentToken = tokens.selectNext()
            nextToken = tokens.selectNext()

            if currentToken.type == T_EOE:
                continue

            if currentToken.type == T_PLUS and nextToken.type == T_INT:
                accumulator += nextToken.value
            elif currentToken.type == T_MINUS and nextToken.type == T_INT:
                accumulator -= nextToken.value
            else:
                errorMessage = f"Invalid expression. {currentToken} {nextToken}"
                raise InvalidExpression(errorMessage)

        return accumulator

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


def main(case):
    result = Parser.run(case)
    print(result)
    return result


if __name__ == '__main__':
    case = argv[1]
    main(case)
