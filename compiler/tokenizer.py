
from .token import (T_CBRACKET, T_DIV, T_EOE, T_INT, T_MINUS, T_MULTI,
                            T_OBRACKET, T_PLUS, Token)
from .errors import InvalidToken


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
