# types
T_INT = 'int'
T_PLUS = 'plus'
T_MINUS = 'minus'
T_MULTI = 'multi'
T_DIV = 'div'
T_EOE = 'end_of_expression'
T_OBRACKET = '('
T_CBRACKET = ')'

T_IDENTIFIER = 'identifier'
T_RESERVED = 'reserved'
T_ASSIGNMENT = 'assignment'

T_O_CURLYBRACKET = '{'
T_C_CURLYBRACKET = '}'
T_SEMICOLON = ';'


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value != None:
            return f'<{self.type}:{self.value}>'
        return f'<{self.type}>'
