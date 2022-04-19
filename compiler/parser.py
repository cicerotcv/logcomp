from .errors import SyntaxError
from .node import (Assignment, BinOp, Block, Identifier, IntVal, NoOp,
                   Reserved, UnOp)
from .token import (T_ASSIGNMENT, T_C_CURLYBRACKET, T_CBRACKET, T_DIV, T_EOE,
                    T_IDENTIFIER, T_INT, T_MINUS, T_MULTI, T_O_CURLYBRACKET,
                    T_OBRACKET, T_PLUS, T_RESERVED, T_SEMICOLON)
from .tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parse_block():

        tokens = Parser.tokens

        if tokens.current.type != T_O_CURLYBRACKET:
            raise SyntaxError(f"Missing block starting curly bracket.")
        tokens.select_next()

        block = Block(None, [])

        while tokens.current.type != T_C_CURLYBRACKET:
            block.children.append(Parser.parse_statement())

        tokens.select_next()

        return block

    @staticmethod
    def parse_statement():
        tokens = Parser.tokens
        statement = NoOp(None)

        if tokens.current.type == T_IDENTIFIER:
            identifier = Identifier(tokens.current.value)
            tokens.select_next()

            if tokens.current.type != T_ASSIGNMENT:
                raise SyntaxError(
                    f"Expected '{T_ASSIGNMENT}' and got {tokens.current.type}")

            tokens.select_next()  # consome '='

            statement = Assignment(
                'assignment', [identifier, Parser.parse_expression()])

        elif tokens.current.type == T_RESERVED:
            reserved = tokens.current
            tokens.select_next()

            if tokens.current.type != T_OBRACKET:
                raise SyntaxError(
                    f"Expected '{T_OBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement = Reserved(reserved.value, [Parser.parse_expression()])

            if tokens.current.type != T_CBRACKET:
                raise SyntaxError(
                    f"Expected '{T_CBRACKET}' and got '{tokens.current.type}'")

            tokens.select_next()

        if tokens.current.type != T_SEMICOLON:
            raise SyntaxError(f"Expected semicolon and got '{tokens.current}'")

        tokens.select_next()

        return statement

    @staticmethod
    def parse_expression():
        tokens = Parser.tokens

        N = Parser.parse_term()

        if tokens.current.type == T_INT:
            raise SyntaxError(f"Unexpected token: {tokens.current}")

        while tokens.current.type in [T_PLUS, T_MINUS]:

            if tokens.current.type == T_PLUS:
                tokens.select_next()
                # N += Parser.parse_term()
                N = BinOp(T_PLUS, [N, Parser.parse_term()])

            elif tokens.current.type == T_MINUS:
                tokens.select_next()
                # N -= Parser.parse_term()
                N = BinOp(T_MINUS, [N, Parser.parse_term()])

        return N

    @staticmethod
    def parse_term():
        tokens = Parser.tokens

        N = Parser.parse_factor()  # node

        while tokens.current.type in [T_DIV, T_MULTI]:

            if tokens.current.type == T_DIV:
                tokens.select_next()
                # N = int(N / Parser.parse_factor())
                N = BinOp(T_DIV, [N, Parser.parse_factor()])

            elif tokens.current.type == T_MULTI:
                tokens.select_next()
                # N = int(N * Parser.parse_factor())
                N = BinOp(T_MULTI, [N, Parser.parse_factor()])

            else:
                error_message = f'Expected "*", "/", "+" or "-" and got {tokens.current}'
                raise SyntaxError(error_message)

        return N

    @staticmethod
    def parse_factor():
        tokens = Parser.tokens

        if tokens.current.type == T_INT:
            N = IntVal(tokens.current.value)
            tokens.select_next()

        elif tokens.current.type == T_IDENTIFIER:
            N = Identifier(tokens.current.value)
            tokens.select_next()

        elif tokens.current.type == T_PLUS:
            tokens.select_next()
            # N = Parser.parse_factor()
            N = UnOp(T_PLUS, [Parser.parse_factor()])

        elif tokens.current.type == T_MINUS:
            tokens.select_next()
            # N = -Parser.parse_factor()
            N = UnOp(T_MINUS, [Parser.parse_factor()])

        elif tokens.current.type == T_OBRACKET:
            tokens.select_next()
            # N = Parser.parse_expression()
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
        block = Parser.parse_block()
        if Parser.tokens.current.type != T_EOE:
            raise SyntaxError(f"Unexpected token: {Parser.tokens.current}")
        return block
