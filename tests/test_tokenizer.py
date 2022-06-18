import pytest
from compiler.constants import (D_C_CURLYBRACKET, D_CBRACKET, D_COMMA, D_O_CURLYBRACKET,
                                D_OBRACKET, D_SEMICOLON, LOG_AND, LOG_EQ,
                                LOG_GT, LOG_LT, LOG_OR, OP_ASSIGNMENT, OP_CONCAT, OP_DIV,
                                OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, R_ELSE,
                                R_IF, R_PRINTF, R_RETURN, R_SCANF, R_WHILE, T_EOE,
                                T_IDENTIFIER, T_INT, T_STR, T_TYPE, T_VOID)
from compiler.token import Token
from compiler.tokenizer import Tokenizer
from compiler.errors import UnclosingDelimiter, InvalidToken


def compare_token(a: Token, b: Token):
    assert a.type == b.type
    assert a.value == b.value


class TestBuiltins:

    @staticmethod
    def test_integer_one_digit():
        origin = '7'
        token = Tokenizer(origin).select_next()
        expected = Token(T_INT, 7)
        compare_token(token, expected)

    @staticmethod
    def test_integer_two_digit():
        origin = '18'
        token = Tokenizer(origin).select_next()
        expected = Token(T_INT, 18)
        compare_token(token, expected)

    @staticmethod
    def test_empty_string():
        origin = '\"\"'
        token = Tokenizer(origin).select_next()
        expected = Token(T_STR, '')
        compare_token(token, expected)

    @staticmethod
    def test_single_quote_exception():
        origin = '\'Single Comma String\''
        with pytest.raises(InvalidToken):
            Tokenizer(origin).select_next()

    @staticmethod
    def test_string_word():
        origin = '"word"'
        token = Tokenizer(origin).select_next()
        expected = Token(T_STR, "word")
        compare_token(token, expected)

    @staticmethod
    def test_string_sentence():
        origin = '"this is a sentence"'
        token = Tokenizer(origin).select_next()
        expected = Token(T_STR, "this is a sentence")
        compare_token(token, expected)

    @staticmethod
    def test_unclosing_string_exception():
        origin = '"this is an unclosed string'
        with pytest.raises(UnclosingDelimiter):
            Tokenizer(origin).select_next()

    @staticmethod
    def test_typing_str():
        origin = 'str'
        token = Tokenizer(origin).select_next()
        expected = Token(T_TYPE, T_STR)
        compare_token(token, expected)

    @staticmethod
    def test_typing_int():
        origin = 'int'
        token = Tokenizer(origin).select_next()
        expected = Token(T_TYPE, T_INT)
        compare_token(token, expected)

    @staticmethod
    def test_typing_void():
        origin = 'void'
        token = Tokenizer(origin).select_next()
        expected = Token(T_TYPE, T_VOID)
        compare_token(token, expected)

    @staticmethod
    def test_typing_str_identifier():
        origin = 'str string_name'
        tokenizer = Tokenizer(origin)
        type_token = tokenizer.select_next()
        identifier = tokenizer.select_next()
        expected_type_token = Token(T_TYPE, T_STR)
        expected_identifier = Token(T_IDENTIFIER, 'string_name')
        compare_token(type_token, expected_type_token)
        compare_token(identifier, expected_identifier)

    @staticmethod
    def test_typing_int_identifier():
        origin = 'int number_identifier'
        tokenizer = Tokenizer(origin)
        type_token = tokenizer.select_next()
        expected_type_token = Token(T_TYPE, T_INT)
        identifier = tokenizer.select_next()
        expected_identifier = Token(T_IDENTIFIER, 'number_identifier')
        compare_token(type_token, expected_type_token)
        compare_token(identifier, expected_identifier)


class TestOperations:
    @staticmethod
    def test_plus():
        origin = "+"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_PLUS))

    @staticmethod
    def test_minus():
        origin = "-"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_MINUS))

    @staticmethod
    def test_multiplication():
        origin = "*"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_MULTI))

    @staticmethod
    def test_concat():
        origin = "."
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_CONCAT))

    @staticmethod
    def test_division():
        origin = "/"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_DIV))

    @staticmethod
    def test_assignment():
        origin = "!"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_NOT))

    @staticmethod
    def test_assignment():
        origin = "="
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(OP_ASSIGNMENT))


class TestDelimiters:
    @staticmethod
    def test_opening_bracket():
        origin = "("
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_OBRACKET))

    @staticmethod
    def test_closing_bracket():
        origin = ")"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_CBRACKET))

    @staticmethod
    def test_opening_curly_bracket():
        origin = "{"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_O_CURLYBRACKET))

    @staticmethod
    def test_closing_curly_bracket():
        origin = "}"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_C_CURLYBRACKET))

    @staticmethod
    def test_semicolon():
        origin = ";"
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_SEMICOLON))

    @staticmethod
    def test_semicolon():
        origin = ","
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(D_COMMA))


class TestLogicalOperators:
    @staticmethod
    def test_logical_or():
        origin = '||'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(LOG_OR))

    @staticmethod
    def test_logical_and():
        origin = '&&'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(LOG_AND))

    @staticmethod
    def test_logical_equal():
        origin = '=='
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(LOG_EQ))

    @staticmethod
    def test_logical_greater_than():
        origin = '>'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(LOG_GT))

    @staticmethod
    def test_logical_less_than():
        origin = '<'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(LOG_LT))


class TestReservedWords:
    @staticmethod
    def test_printf():
        origin = 'printf'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_PRINTF))

    @staticmethod
    def test_scanf():
        origin = 'scanf'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_SCANF))

    @staticmethod
    def test_while():
        origin = 'while'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_WHILE))

    @staticmethod
    def test_if():
        origin = 'if'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_IF))

    @staticmethod
    def test_else():
        origin = 'else'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_ELSE))

    @staticmethod
    def test_else():
        origin = 'return'
        token = Tokenizer(origin).select_next()
        compare_token(token, Token(R_RETURN))


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
