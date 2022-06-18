from typing import List

from compiler.constants import (LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR, OP_CONCAT,
                                OP_DIV, OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, T_FUNCTION, T_INT, T_STR, T_VOID)
from compiler.errors import FunctionError, OperationError
from compiler.symboltable import FuncTable, SymbolTable


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children: List[Node] = children

    def evaluate(self, symbol_table: SymbolTable = None):
        pass

    def __repr__(self):
        name = self.__class__.__name__
        if self.children is None:
            return f"<{name}:{self.value}>"
        return f"<{name}:{self.value}:[{self.children}]>"


class BinOp(Node):
    """Realiza operações binárias. Contém dois nós filhos
    `value`: operador (`+`, `-`, `*`, `/`, `&&`, `||`, `==`, `>`, `<`, `.`)

    `children[2]`: valores que serão submetidos ao operador 
    
    `children[0]` `<operator>` `children[1]`
    """

    def evaluate(self, symbol_table):
        n1, n2 = self.children
        (type1, value1) = n1.evaluate(symbol_table)
        (type2, value2) = n2.evaluate(symbol_table)

        if self.value == OP_CONCAT:
            return (T_STR, str(value1) + str(value2))

        if type1 != type2:
            raise OperationError(
                f"Unexpected operation for types '{type1}' and '{type2}': '{self.value}'")
        if self.value == OP_PLUS:
            return (T_INT, value1 + value2)
        if self.value == OP_MINUS:
            return (T_INT, value1 - value2)
        if self.value == OP_MULTI:
            return (T_INT, value1 * value2)
        if self.value == OP_DIV:
            return (T_INT, value1 // value2)
        if self.value == LOG_AND:
            return (T_INT, int(value1 and value2))
        if self.value == LOG_OR:
            return (T_INT, int(value1 or value2))
        if self.value == LOG_EQ:
            return (T_INT, int(value1 == value2))
        if self.value == LOG_GT:
            return (T_INT, int(value1 > value2))
        if self.value == LOG_LT:
            return (T_INT, int(value1 < value2))

        raise OperationError(f"Unexpected value for BinOp: '{self.value}'")


class UnOp(Node):
    """Realiza operações unárias. Contém um único nó filho
    
    `value`: operador (`!`, `-`, `+`)

    `children[1]`: valor
    """

    def evaluate(self, symbol_table):
        node = self.children[0]
        (type, value) = node.evaluate(symbol_table)

        if type != T_INT:
            raise OperationError(
                f"Unexpected unary operator '{self.value}' for type '{type}'")

        if self.value == OP_MINUS:
            return (T_INT, -value)
        if self.value == OP_PLUS:
            return (T_INT, value)
        if self.value == OP_NOT:
            return (T_INT, int(not value))

        raise OperationError(f"Unexpected value for UnOp: '{self.value}'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self, symbol_table):
        return (T_INT, self.value)


class StrVal(Node):
    """Valor de string. Contém um único nó filho"""

    def evaluate(self, symbol_table):
        return (T_STR, self.value)


class NoOp(Node):
    def evaluate(self, symbol_table):
        pass


class Identifier(Node):
    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)


class Assignment(Node):
    def evaluate(self, symbol_table):
        identifier, value = self.children
        symbol_table.set(identifier.value, value.evaluate(symbol_table))


class Printf(Node):
    def evaluate(self, symbol_table):
        (_, value) = self.children[0].evaluate(symbol_table)
        print(value)


class Scanf(Node):
    def evaluate(self, symbol_table):
        # return int(input("Insira um número para o scanf: "))
        return (T_INT, int(input()))


class VarDec(Node):
    """
    `value`: tipo

    `children`: nomes de identifiers
    """

    def evaluate(self, symbol_table):
        type = self.value
        for identifier_name in self.children:
            symbol_table.declare(type, identifier_name)


class FuncDec(Node):
    """`value`: Nome da função;

    `children[n]`: `VarDec` e Block. Os argumentos da declaração devem
    ser incorporados ao `VarDec`, incluindo o próprio nome da função e seu tipo
    correspondente.

    O `evaluate()` apenas cria uma variável na `SymbolTable` atual, sendo o nome
    da variável o nome da função, o valor apontando para o próprio nó `FuncDec`
    e o tipo será `T_FUNCTION`"""

    def evaluate(self, symbol_table):
        # symbol_table.declare(T_FUNCTION, self.value)
        symbol_table.declare(T_FUNCTION, self.value)
        symbol_table.set(self.value, self)


class FuncCall(Node):
    """`value`: nome da função;

    `children[n]`: possui `n` filhos do tipo identificador ou expressão. 
    São os argumentos da chamada.

    O `evaluate()` vai realizar o verdadeiro `evaluate()` da `FuncDec`,
    recuperando o nó de declaração na `SymbolTable`, atribuindo os valores dos
    argumentos de entrada e executando o bloco (segundo filho)."""

    def evaluate(self, symbol_table):
        func_dec: FuncDec = FuncTable.get(self.value)

        new_symbol_table = SymbolTable()

        # var_dec é a declaração de argumentos na SymbolTable local
        # var_dec, *statements = func_dec.children

        # self_dec é a declaração da própria função "tipo nome(...)"
        # arg_decs são as declarações de cada argumento da função
        # block é a definição do que ocorre dentro da função
        self_dec, *arg_decs, block = func_dec.children

        self_dec.evaluate(new_symbol_table)

        values = self.children

        if len(arg_decs) != len(values):
            raise FunctionError(f"Number of arguments does not match the required number: Called with {len(values)}; Expected {len(arg_decs)}")

        for var_dec, value in zip(arg_decs, values):
            var_dec.evaluate(new_symbol_table)
            new_symbol_table.set(var_dec.children[0], symbol_table.get(value.value))


        (type, value) = block.evaluate(new_symbol_table)

        expected_type = self_dec.value

        if type != expected_type:
            raise FunctionError(f"Type '{type}' doesn't match the expected return type '{expected_type}'")
        
        return (type, value)


class Return(Node):
    """
    `value`: type

    `children[1]`: value
    """
    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)


class While(Node):
    def evaluate(self, symbol_table):
        condition, routine = self.children
        (_, evaluation) = condition.evaluate(symbol_table)

        while evaluation:
            routine.evaluate(symbol_table)
            (_, evaluation) = condition.evaluate(symbol_table)


class If(Node):
    def evaluate(self, symbol_table):
        # if { expression } : { this } else: { that }
        if len(self.children) == 3:
            expression, this, that = self.children
            (_, evaluation) = expression.evaluate(symbol_table)
            if (evaluation):
                this.evaluate(symbol_table)
            else:
                that.evaluate(symbol_table)

        # if { expression } : { this }
        if len(self.children) == 2:
            expression, this = self.children
            (_, evaluation) = expression.evaluate(symbol_table)
            if (evaluation):
                this.evaluate(symbol_table)


class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            block_return = child.evaluate(symbol_table)
            if block_return is not None:
                return block_return
        return (T_VOID, None)
