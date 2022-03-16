# -*- encoding: utf-8 -*-
from sys import argv

# types
T_INT = 'int'
T_PLUS = 'plus'
T_MINUS = 'minus'
T_MULTI = 'multi'
T_DIV = 'div'
T_EOE = 'end_of_expression'
T_OBRACKET = '(_'
T_CBRACKET = '_)'

# errors
E_TOKEN_ERROR = 'invalid_token'
E_SYNTAX_ERROR = 'syntax_error'


class Error(Exception):
    def __init__(self, type, description):
        super().__init__(f'{type} :: {description}')


class InvalidToken(Error):
    def __init__(self, description) -> None:
        super().__init__(E_TOKEN_ERROR, description)


class SyntaxError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_SYNTAX_ERROR, description)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value != None:
            return f'<{self.type}:{self.value}>'
        return f'<{self.type}>'


class PrePro:
    @staticmethod
    def filter(expression):
        start = expression.find('/*')

        if start == -1:
            return expression

        end = expression.find('*/')

        if end == -1:
            return SyntaxError("Comment block doesn't close")

        replace_string = expression[start:end + 2]
        expression = expression.replace(replace_string, '', 1)

        return PrePro.filter(expression)


class Tokenizer:
    def __init__(self, origin: str):
        self.origin: str = origin
        self.position: int = 0
        self.current: Token = None

    def select_next(self):

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

        if self.origin[self.position] == '/':
            self.current = Token(T_DIV)
            self.position += 1
            return self.current

        if self.origin[self.position] == '*':
            self.current = Token(T_MULTI)
            self.position += 1
            return self.current

        if self.origin[self.position] == '+':
            self.current = Token(T_PLUS)
            self.position += 1
            return self.current

        if self.origin[self.position] == '-':
            self.current = Token(T_MINUS)
            self.position += 1
            return self.current

        if self.origin[self.position] == '(':
            self.current = Token(T_OBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == ')':
            self.current = Token(T_CBRACKET)
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
        raise InvalidToken(f"Unrecognized token '{tokenValue}'")


class Parser:
    tokens = None

    @staticmethod
    def parse_expression():
        tokens = Parser.tokens

        N = Parser.parse_term()

        # if tokens.current.type not in [T_PLUS, T_MINUS, T_EOE]:
        #     error_message = f'Expected "+" or "-" and got "{tokens.current}"'
        #     raise SyntaxError(error_message)

        while tokens.current.type in [T_PLUS, T_MINUS]:

            if tokens.current.type == T_PLUS:
                tokens.select_next()
                N += Parser.parse_term()

            elif tokens.current.type == T_MINUS:
                tokens.select_next()
                N -= Parser.parse_term()

        return N

    @staticmethod
    def parse_term():
        tokens = Parser.tokens

        N = Parser.parse_factor()  # number

        while tokens.current.type in [T_DIV, T_MULTI]:

            if tokens.current.type == T_DIV:
                tokens.select_next()
                number = Parser.parse_factor()
                N = int(N / number)

            elif tokens.current.type == T_MULTI:
                tokens.select_next()
                number = Parser.parse_factor()
                N = int(N * number)

            else:
                error_message = f'Expected "*", "/", "+" or "-" and got {tokens.current}'
                raise SyntaxError(error_message)

        return N

    @staticmethod
    def parse_factor():
        tokens = Parser.tokens

        if tokens.current.type == T_INT:
            N = tokens.current.value
            tokens.select_next()

        elif tokens.current.type == T_PLUS:
            tokens.select_next()
            N = Parser.parse_factor()

        elif tokens.current.type == T_MINUS:
            tokens.select_next()
            N = -Parser.parse_factor()

        elif tokens.current.type == T_OBRACKET:
            tokens.select_next()
            N = Parser.parse_expression()

            if tokens.current.type != T_CBRACKET:
                raise SyntaxError("Bracket doesn't close")

            tokens.select_next()

        else:
            raise SyntaxError(f"Unexpected token {tokens.current}")

        return N

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.select_next()
        return Parser.parse_expression()


def main(case):
    processed = PrePro.filter(case)
    result = Parser.run(processed)
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
    
