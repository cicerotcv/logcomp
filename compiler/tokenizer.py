
from string import ascii_letters, digits

from compiler.constants import (D_C_CURLYBRACKET, D_CBRACKET, D_COMMA,
                                D_O_CURLYBRACKET, D_OBRACKET, D_SEMICOLON,
                                LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR,
                                OP_ASSIGNMENT, OP_CONCAT, OP_DIV, OP_MINUS,
                                OP_MULTI, OP_NOT, OP_PLUS, R_ELSE, R_IF,
                                R_PRINTF, R_RETURN, R_SCANF, R_WHILE, T_EOE,
                                T_IDENTIFIER, T_INT, T_STR, T_TYPE, T_VOID)
from compiler.errors import InvalidToken, UnclosingDelimiter
from compiler.token import Token

ALLOWED_CHARS = ascii_letters + digits + "_"
STRING_DELIMITERS = ['\"']
BUILTIN_TYPES = [T_INT, T_STR, T_VOID]

RESERVED_WORDS = {
    R_PRINTF: R_PRINTF,
    R_SCANF: R_SCANF,
    R_WHILE: R_WHILE,
    R_IF: R_IF,
    R_ELSE: R_ELSE,
    T_INT: T_INT,
    T_STR: T_STR,
    T_VOID: T_VOID,
    R_RETURN: R_RETURN
}


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
        while self.origin[self.position] in [' ', '\n']:
            self.position += 1
            if self.position >= len(self.origin):
                self.current = Token(T_EOE)
                return self.current

        if self.origin[self.position] == '/':
            self.current = Token(OP_DIV)
            self.position += 1
            return self.current

        if self.origin[self.position] == '*':
            self.current = Token(OP_MULTI)
            self.position += 1
            return self.current

        if self.origin[self.position] == '.':
            self.current = Token(OP_CONCAT)
            self.position += 1
            return self.current

        if self.origin[self.position] == '+':
            self.current = Token(OP_PLUS)
            self.position += 1
            return self.current

        if self.origin[self.position] == '-':
            self.current = Token(OP_MINUS)
            self.position += 1
            return self.current

        if self.origin[self.position] == '(':
            self.current = Token(D_OBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == ')':
            self.current = Token(D_CBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == '{':
            self.current = Token(D_O_CURLYBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == '}':
            self.current = Token(D_C_CURLYBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == '=':
            self.position += 1
            if self.position < len(self.origin) and self.origin[self.position] == '=':
                self.current = Token(LOG_EQ)
                self.position += 1
            else:
                self.current = Token(OP_ASSIGNMENT)
            return self.current

        if self.origin[self.position] == ';':
            self.current = Token(D_SEMICOLON)
            self.position += 1
            return self.current

        if self.origin[self.position] == ',':
            self.current = Token(D_COMMA)
            self.position += 1
            return self.current

        if self.origin[self.position] == '|':
            self.position += 1

            if self.position >= len(self.origin) or self.origin[self.position] != "|":
                raise InvalidToken(f"Expected '||' and got '|'")

            self.position += 1
            self.current = Token(LOG_OR)
            return self.current

        if self.origin[self.position] == '&':
            self.position += 1

            if self.position >= len(self.origin) or self.origin[self.position] != "&":
                raise InvalidToken(f"Expected '&&' and got '&'")

            self.position += 1
            self.current = Token(LOG_AND)
            return self.current

        if self.origin[self.position] == '<':
            self.current = Token(LOG_LT)
            self.position += 1
            return self.current

        if self.origin[self.position] == '>':
            self.current = Token(LOG_GT)
            self.position += 1
            return self.current

        if self.origin[self.position] == '!':
            self.current = Token(OP_NOT)
            self.position += 1
            return self.current

        if self.origin[self.position] in STRING_DELIMITERS:
            opening = self.origin[self.position]
            string = ''
            self.position += 1

            if self.position >= len(self.origin):
                raise UnclosingDelimiter(f"Expected string delimiter to close")

            while self.origin[self.position] != opening:
                string += self.origin[self.position]
                self.position += 1

                if self.position >= len(self.origin):
                    raise UnclosingDelimiter(
                        f"Expected string delimiter to close")

            self.current = Token(T_STR, string)
            self.position += 1
            return self.current

        # garante que inicial com caractere
        if self.origin[self.position].isalpha():
            candidate = ''

            while self.origin[self.position] in ALLOWED_CHARS:
                candidate += self.origin[self.position]
                self.position += 1
                if self.position >= len(self.origin):
                    break

            if candidate in BUILTIN_TYPES:
                self.current = Token(T_TYPE, candidate)
            elif candidate in RESERVED_WORDS.keys():
                self.current = Token(RESERVED_WORDS[candidate])
            else:
                self.current = Token(T_IDENTIFIER, candidate)

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
