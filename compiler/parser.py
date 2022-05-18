from compiler.constants import (D_C_CURLYBRACKET, D_CBRACKET, D_COMMA,
                                D_O_CURLYBRACKET, D_OBRACKET, D_SEMICOLON,
                                LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR,
                                OP_ASSIGNMENT, OP_CONCAT, OP_DIV, OP_MINUS, OP_MULTI,
                                OP_NOT, OP_PLUS, R_ELSE, R_IF, R_PRINTF,
                                R_SCANF, R_WHILE, T_EOE, T_IDENTIFIER, T_INT, T_STR,
                                T_TYPE)
from compiler.errors import SyntaxError
from compiler.node import (Assignment, BinOp, Block, Identifier, If, IntVal,
                           NoOp, Printf, Scanf, StrVal, UnOp, VarDec, While)
from compiler.tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parse_block():

        tokens = Parser.tokens

        if tokens.current.type != D_O_CURLYBRACKET:
            raise SyntaxError(f"Missing block starting curly bracket.")
        tokens.select_next()

        block = Block(None, [])

        while tokens.current.type != D_C_CURLYBRACKET:
            block.children.append(Parser.parse_statement())

        tokens.select_next()

        return block

    @staticmethod
    def parse_statement():
        tokens = Parser.tokens
        statement = NoOp(None)

        if tokens.current.type == D_SEMICOLON:
            tokens.select_next()

        elif tokens.current.type == T_IDENTIFIER:
            identifier = Identifier(tokens.current.value)
            tokens.select_next()

            if tokens.current.type != OP_ASSIGNMENT:
                raise SyntaxError(
                    f"Expected '{OP_ASSIGNMENT}' and got {tokens.current.type}")

            tokens.select_next()

            statement = Assignment(
                'assignment', [identifier, Parser.parse_rel_expression()])

            if tokens.current.type != D_SEMICOLON:
                raise SyntaxError(
                    f"Expected semicolon and got '{tokens.current}'")

            tokens.select_next()

        elif tokens.current.type == R_PRINTF:
            reserved = tokens.current
            tokens.select_next()

            if tokens.current.type != D_OBRACKET:
                raise SyntaxError(
                    f"Expected '{D_OBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement = Printf(reserved.value, [Parser.parse_rel_expression()])

            if tokens.current.type != D_CBRACKET:
                raise SyntaxError(
                    f"Expected '{D_CBRACKET}' and got '{tokens.current.type}'")

            tokens.select_next()

            if tokens.current.type != D_SEMICOLON:
                raise SyntaxError(
                    f"Expected semicolon and got '{tokens.current}'")

            tokens.select_next()

        elif tokens.current.type == T_TYPE:
            statement = VarDec(tokens.current.value, [])
            tokens.select_next()

            if tokens.current.type != T_IDENTIFIER:
                raise SyntaxError(
                    f"Expected '{T_IDENTIFIER}' and got {tokens.current}")

            statement.children.append(tokens.current.value)
            tokens.select_next()

            while tokens.current.type == D_COMMA:
                tokens.select_next()

                if tokens.current.type != T_IDENTIFIER:
                    raise SyntaxError(
                        f"Expected '{T_IDENTIFIER}' and got {tokens.current}")

                statement.children.append((tokens.current.value))
                tokens.select_next()

            if tokens.current.type != D_SEMICOLON:
                raise SyntaxError(
                    f"Expected semicolon and got '{tokens.current}'")

            tokens.select_next()

        elif tokens.current.type == R_WHILE:
            statement = While(tokens.current.value, [])
            tokens.select_next()

            if tokens.current.type != D_OBRACKET:
                raise SyntaxError(
                    f"Expected '{D_OBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement.children.append(Parser.parse_rel_expression())

            if tokens.current.type != D_CBRACKET:
                raise SyntaxError(
                    f"Expected '{D_CBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement.children.append(Parser.parse_statement())

        elif tokens.current.type == R_IF:
            statement = If(tokens.current.value, [])
            tokens.select_next()

            if tokens.current.type != D_OBRACKET:
                raise SyntaxError(
                    f"Expected '{D_OBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement.children.append(Parser.parse_rel_expression())

            if tokens.current.type != D_CBRACKET:
                raise SyntaxError(
                    f"Expected '{D_CBRACKET}' and got '{tokens.current.type}'")
            tokens.select_next()

            statement.children.append(Parser.parse_statement())

            if tokens.current.type == R_ELSE:
                tokens.select_next()
                statement.children.append(Parser.parse_statement())

        else:
            statement = Parser.parse_block()

        return statement

    @staticmethod
    def parse_rel_expression():
        tokens = Parser.tokens

        N = Parser.parse_expression()

        while tokens.current.type in [LOG_EQ, LOG_GT, LOG_LT]:

            if tokens.current.type == LOG_EQ:
                tokens.select_next()
                N = BinOp(LOG_EQ, [N, Parser.parse_expression()])

            elif tokens.current.type == LOG_GT:
                tokens.select_next()
                N = BinOp(LOG_GT, [N, Parser.parse_expression()])

            elif tokens.current.type == LOG_LT:
                tokens.select_next()
                N = BinOp(LOG_LT, [N, Parser.parse_expression()])

        return N

    @staticmethod
    def parse_expression():
        tokens = Parser.tokens

        N = Parser.parse_term()

        if tokens.current.type == T_INT:
            raise SyntaxError(f"Unexpected token: {tokens.current}")

        while tokens.current.type in [OP_PLUS, OP_MINUS, LOG_OR, OP_CONCAT]:

            if tokens.current.type == OP_PLUS:
                tokens.select_next()
                N = BinOp(OP_PLUS, [N, Parser.parse_term()])

            elif tokens.current.type == OP_MINUS:
                tokens.select_next()
                N = BinOp(OP_MINUS, [N, Parser.parse_term()])

            elif tokens.current.type == LOG_OR:
                tokens.select_next()
                N = BinOp(LOG_OR, [N, Parser.parse_term()])

            elif tokens.current.type == OP_CONCAT:
                tokens.select_next()
                N = BinOp(OP_CONCAT, [N, Parser.parse_expression()])

        return N

    @staticmethod
    def parse_term():
        tokens = Parser.tokens

        N = Parser.parse_factor()  # node

        while tokens.current.type in [OP_DIV, OP_MULTI, LOG_AND]:

            if tokens.current.type == OP_DIV:
                tokens.select_next()
                N = BinOp(OP_DIV, [N, Parser.parse_factor()])

            elif tokens.current.type == OP_MULTI:
                tokens.select_next()
                N = BinOp(OP_MULTI, [N, Parser.parse_factor()])

            elif tokens.current.type == LOG_AND:
                tokens.select_next()
                N = BinOp(LOG_AND, [N, Parser.parse_factor()])

            else:
                error_message = f'Unexpected {tokens.current}'
                raise SyntaxError(error_message)

        return N

    @staticmethod
    def parse_factor():
        tokens = Parser.tokens

        if tokens.current.type == T_INT:
            N = IntVal(tokens.current.value)
            tokens.select_next()

        elif tokens.current.type == T_STR:
            N = StrVal(tokens.current.value)
            tokens.select_next()

        elif tokens.current.type == T_IDENTIFIER:
            N = Identifier(tokens.current.value)
            tokens.select_next()

        elif tokens.current.type == OP_PLUS:
            tokens.select_next()
            N = UnOp(OP_PLUS, [Parser.parse_factor()])

        elif tokens.current.type == OP_MINUS:
            tokens.select_next()
            N = UnOp(OP_MINUS, [Parser.parse_factor()])

        elif tokens.current.type == OP_NOT:
            tokens.select_next()
            N = UnOp(OP_NOT, [Parser.parse_factor()])

        elif tokens.current.type == D_OBRACKET:
            tokens.select_next()

            N = Parser.parse_rel_expression()

            if tokens.current.type != D_CBRACKET:
                raise SyntaxError(f"Expected ')' and got {tokens.current}")

            tokens.select_next()

        elif tokens.current.type == R_SCANF:
            N = Scanf('scanf')

            tokens.select_next()

            if tokens.current.type != D_OBRACKET:
                raise SyntaxError(f"Expected '(' and got {tokens.current}")

            tokens.select_next()

            if tokens.current.type != D_CBRACKET:
                raise SyntaxError(f"Expected ')' and got {tokens.current}")

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
