
from .token import (T_ASSIGNMENT, T_C_CURLYBRACKET, T_CBRACKET, T_DIV, T_EOE, T_IDENTIFIER, T_INT, T_MINUS, T_MULTI, T_O_CURLYBRACKET,
                    T_OBRACKET, T_PLUS, T_RESERVED, T_SEMICOLON, Token)
from .errors import InvalidToken

from string import ascii_letters, digits

ALLOWED_CHARS = ascii_letters + digits + "_"
RESERVED_WORDS = ['printf']


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

        if self.origin[self.position] == '{':
            self.current = Token(T_O_CURLYBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == '}':
            self.current = Token(T_C_CURLYBRACKET)
            self.position += 1
            return self.current

        if self.origin[self.position] == '=':
            self.current = Token(T_ASSIGNMENT)
            self.position += 1
            return self.current

        if self.origin[self.position] == ';':
            self.current = Token(T_SEMICOLON)
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

            if candidate in RESERVED_WORDS:
                self.current = Token(T_RESERVED, candidate)
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
