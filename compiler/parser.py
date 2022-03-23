from .token import (T_CBRACKET, T_DIV, T_EOE, T_INT, T_MINUS, T_MULTI,
                    T_OBRACKET, T_PLUS)
from .errors import SyntaxError
from .tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parse_expression():
        tokens = Parser.tokens

        N = Parser.parse_term()

        if tokens.current.type == T_INT:
            raise SyntaxError(f"Unexpected token: {tokens.current}")

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
                N = int(N / Parser.parse_factor())

            elif tokens.current.type == T_MULTI:
                tokens.select_next()
                N = int(N * Parser.parse_factor())

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
                raise SyntaxError("Brackets doesn't close")

            tokens.select_next()

        else:
            raise SyntaxError(f"Unexpected token: {tokens.current}")

        return N

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.select_next()
        N = Parser.parse_expression()
        if Parser.tokens.current.type != T_EOE:
            raise SyntaxError(f"Unexpected token: {Parser.tokens.current}")
        return N
