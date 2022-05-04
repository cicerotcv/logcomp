
from string import ascii_letters, digits
from compiler.token import Token
from compiler.constants import (D_C_CURLYBRACKET, D_CBRACKET, D_O_CURLYBRACKET,
                                D_OBRACKET, D_SEMICOLON, LOG_AND, LOG_EQ,
                                LOG_GT, LOG_LT, LOG_OR, OP_ASSIGNMENT, OP_DIV,
                                OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, R_ELSE,
                                R_IF, R_PRINTF, R_SCANF, R_WHILE, T_EOE, T_IDENTIFIER, T_INT)

from compiler.errors import InvalidToken

ALLOWED_CHARS = ascii_letters + digits + "_"
RESERVED_WORDS = {
    R_PRINTF: R_PRINTF,
    R_SCANF: R_SCANF,
    R_WHILE: R_WHILE,
    R_IF: R_IF,
    R_ELSE: R_ELSE
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
            else:
                self.current = Token(OP_ASSIGNMENT)
            return self.current

        if self.origin[self.position] == ';':
            self.current = Token(D_SEMICOLON)
            self.position += 1
            return self.current

        if self.origin[self.position] == '|':
            self.position += 1

            if self.position >= len(self.origin) or self.current[self.position] != "|":
                raise InvalidToken(f"Expected '||' and got '|'")

            self.position += 1
            self.current = Token(LOG_OR)
            return self.current

        if self.origin[self.position] == '&':
            self.position += 1

            if self.position >= len(self.origin) or self.current[self.position] != "&":
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

        # garante que inicial com caractere
        if self.origin[self.position].isalpha():
            candidate = ''

            while self.origin[self.position] in ALLOWED_CHARS:
                candidate += self.origin[self.position]
                self.position += 1
                if self.position >= len(self.origin):
                    break

            if candidate in RESERVED_WORDS.keys():
                self.current = Token(RESERVED_WORDS[candidate], candidate)
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
