from compiler.constants import (D_C_CURLYBRACKET, D_CBRACKET, D_O_CURLYBRACKET,
                                D_OBRACKET, D_SEMICOLON, LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR, OP_ASSIGNMENT, OP_DIV,
                                OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, T_EOE,
                                T_IDENTIFIER, T_INT)
from compiler.token import Token
from compiler.tokenizer import Tokenizer


class TestBuiltins:
    @staticmethod
    def test_integer_one_digit():
        origin = '7'
        token = Tokenizer(origin).select_next()
        expected = Token(T_INT, 7)
        assert expected.type == token.type
        assert expected.value == token.value

    @staticmethod
    def test_integer_two_digit():
        origin = '18'
        token = Tokenizer(origin).select_next()
        expected = Token(T_INT, 18)
        assert expected.type == token.type
        assert expected.value == token.value


class TestOperations:
    @staticmethod
    def test_plus():
        origin = "+"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_PLUS

    @staticmethod
    def test_minus():
        origin = "-"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_MINUS

    @staticmethod
    def test_multiplication():
        origin = "*"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_MULTI

    @staticmethod
    def test_division():
        origin = "/"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_DIV

    @staticmethod
    def test_assignment():
        origin = "!"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_NOT

    @staticmethod
    def test_assignment():
        origin = "="
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == OP_ASSIGNMENT


class TestDelimiters:
    @staticmethod
    def test_opening_bracket():
        origin = "("
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == D_OBRACKET

    @staticmethod
    def test_closing_bracket():
        origin = ")"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == D_CBRACKET

    @staticmethod
    def test_opening_curly_bracket():
        origin = "{"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == D_O_CURLYBRACKET

    @staticmethod
    def test_closing_curly_bracket():
        origin = "}"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == D_C_CURLYBRACKET

    @staticmethod
    def test_semicolon():
        origin = ";"
        token = Tokenizer(origin).select_next()
        assert token.value is None
        assert token.type == D_SEMICOLON


class TestLogicalOperators:
    @staticmethod
    def test_logical_or():
        origin = '||'
        token = Tokenizer(origin).select_next()
        expected = Token(LOG_OR)
        assert token.type == expected.type
        assert token.value is None

    @staticmethod
    def test_logical_and():
        origin = '&&'
        token = Tokenizer(origin).select_next()
        expected = Token(LOG_AND)
        assert token.type == expected.type
        assert token.value is None

    @staticmethod
    def test_logical_equal():
        origin = '=='
        token = Tokenizer(origin).select_next()
        expected = Token(LOG_EQ)
        assert token.type == expected.type
        assert token.value is None

    @staticmethod
    def test_logical_greater_than():
        origin = '>'
        token = Tokenizer(origin).select_next()
        expected = Token(LOG_GT)
        assert token.type == expected.type
        assert token.value is None

    @staticmethod
    def test_logical_less_than():
        origin = '<'
        token = Tokenizer(origin).select_next()
        expected = Token(LOG_LT)
        assert token.type == expected.type
        assert token.value is None


class TestReservedWords:
    @staticmethod
    def test_printf():
        origin = 'printf'
        token = Tokenizer(origin).select_next()
        expected = Token('printf')
        assert expected.type == token.type
        assert token.value == origin

    @staticmethod
    def test_scanf():
        origin = 'scanf'
        token = Tokenizer(origin).select_next()
        expected = Token('scanf')
        assert expected.type == token.type
        assert token.value == origin

    @staticmethod
    def test_while():
        origin = 'while'
        token = Tokenizer(origin).select_next()
        expected = Token('while')
        assert expected.type == token.type
        assert token.value == origin

    @staticmethod
    def test_if():
        origin = 'if'
        token = Tokenizer(origin).select_next()
        expected = Token('if')
        assert expected.type == token.type
        assert token.value == origin

    @staticmethod
    def test_else():
        origin = 'else'
        token = Tokenizer(origin).select_next()
        expected = Token('else')
        assert expected.type == token.type
        assert token.value == origin


class TestTokens:
    @staticmethod
    def test_ignore_whitespace():
        origin = "  \n\n  "
        token = Tokenizer(origin).select_next()
        expected = Token(T_EOE)
        assert expected.type == token.type
        assert expected.value == token.value

    @staticmethod
    def test_identifier():
        origin = "x"
        token = Tokenizer(origin).select_next()
        expected = Token(T_IDENTIFIER, 'x')
        assert expected.type == token.type
        assert expected.value == token.value

    @staticmethod
    def test_end_of_expression():
        origin = ""
        token = Tokenizer(origin).select_next()
        expected = Token(T_EOE)
        assert expected.type == token.type
        assert expected.value is None
