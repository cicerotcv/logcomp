from typing import List

from compiler.constants import (LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR,
                                OP_DIV, OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS)
from compiler.errors import OperationError
from compiler.symboltable import SymbolTable


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children: List[Node] = children

    def evaluate(self):
        pass


class BinOp(Node):
    """Realiza operações binárias. Contém dois nós filhos"""

    def evaluate(self):
        n1, n2 = self.children

        if self.value == OP_PLUS:
            return n1.evaluate() + n2.evaluate()
        if self.value == OP_MINUS:
            return n1.evaluate() - n2.evaluate()
        if self.value == OP_MULTI:
            return int(n1.evaluate() * n2.evaluate())
        if self.value == OP_DIV:
            return int(n1.evaluate() / n2.evaluate())
        if self.value == LOG_AND:
            return n1.evaluate() and n2.evaluate()
        if self.value == LOG_OR:
            return n1.evaluate() or n2.evaluate()
        if self.value == LOG_EQ:
            return n1.evaluate() == n2.evaluate()
        if self.value == LOG_GT:
            return n1.evaluate() > n2.evaluate()
        if self.value == LOG_LT:
            return n1.evaluate() < n2.evaluate()

        raise OperationError(f"Unexpected value for BinOp: '{self.value}'")


class UnOp(Node):
    """Realiza operações unárias. Contém um único nó filho"""

    def evaluate(self):
        node = self.children[0]

        if self.value == OP_MINUS:
            return -node.evaluate()
        if self.value == OP_PLUS:
            return node.evaluate()
        if self.value == OP_NOT:
            return not node.evaluate()

        raise OperationError(f"Unexpected value for UnOp: '{self.value}'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self):
        return self.value


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
        print(self.children[0].evaluate())


class Scanf(Node):
    def evaluate(self):
        return int(input("Insira um número para o scanf: "))


class While(Node):
    def evaluate(self):
        condition, routine = self.children
        while condition.evaluate():
            routine.evaluate()


class If(Node):
    def evaluate(self):
        # if { expression } : { this } else: { that }
        if len(self.children) == 3:
            expression, this, that = self.children
            if (expression.evaluate()):
                this.evaluate()
            else:
                that.evaluate()

        # if { expression } : { this }
        if len(self.children) == 2:
            expression, this = self.children
            if (expression.evaluate()):
                this.evaluate()


class Block(Node):
    def evaluate(self):
        for child in self.children:
            child.evaluate()
