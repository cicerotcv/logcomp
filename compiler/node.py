from typing import List

from compiler.constants import (LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR, OP_CONCAT,
                                OP_DIV, OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, T_INT, T_STR)
from compiler.errors import OperationError
from compiler.symboltable import SymbolTable


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children: List[Node] = children

    def evaluate(self):
        pass

    def __repr__(self):
        name = self.__class__.__name__
        if self.children is None:
            return f"<{name}:{self.value}>"
        return f"<{name}:{self.value}:[{self.children}]>"


class BinOp(Node):
    """Realiza operações binárias. Contém dois nós filhos"""

    def evaluate(self):
        n1, n2 = self.children
        (type1, value1) = n1.evaluate()
        (type2, value2) = n2.evaluate()

        if self.value == OP_CONCAT and type1 == T_STR:
            return (T_STR, value1 + str(value2))

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
    """Realiza operações unárias. Contém um único nó filho"""

    def evaluate(self):
        node = self.children[0]
        (type, value) = node.evaluate()

        if type != T_INT:
            raise OperationError(
                f"Unexpected unary operator '{self.value}' for type '{type}'")

        if self.value == OP_MINUS:
            return -value
        if self.value == OP_PLUS:
            return value
        if self.value == OP_NOT:
            return not value

        raise OperationError(f"Unexpected value for UnOp: '{self.value}'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self):
        return (T_INT, self.value)


class StrVal(Node):
    """Valor de string. Contém um único nó filho"""

    def evaluate(self):
        return (T_STR, self.value)


class NoOp(Node):
    def evaluate(self):
        pass


class Identifier(Node):
    def evaluate(self):
        return SymbolTable.get(self.value)


class Assignment(Node):
    def evaluate(self):
        identifier, value = self.children
        SymbolTable.set(identifier.value, value.evaluate())


class Printf(Node):
    def evaluate(self):
        (type, value) = self.children[0].evaluate()
        print((type, value))


class Scanf(Node):
    def evaluate(self):
        # return int(input("Insira um número para o scanf: "))
        return IntVal(int(input())).evaluate()


class VarDec(Node):
    def evaluate(self):
        type = self.value
        for identifier_name in self.children:
            SymbolTable.declare(type, identifier_name)


class While(Node):
    def evaluate(self):
        condition, routine = self.children
        (_, evaluation) = condition.evaluate()

        while evaluation:
            routine.evaluate()
            (_, evaluation) = condition.evaluate()


class If(Node):
    def evaluate(self):
        # if { expression } : { this } else: { that }
        if len(self.children) == 3:
            expression, this, that = self.children
            (_, evaluation) = expression.evaluate()
            if (evaluation):
                this.evaluate()
            else:
                that.evaluate()

        # if { expression } : { this }
        if len(self.children) == 2:
            expression, this = self.children
            (_, evaluation) = expression.evaluate()
            if (evaluation):
                this.evaluate()


class Block(Node):
    def evaluate(self):
        for child in self.children:
            child.evaluate()
