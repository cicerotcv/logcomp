from typing import List

from compiler.token import T_DIV, T_MINUS, T_MULTI, T_PLUS

from .errors import OperationError


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children: List[Node] = children

    def evaluate(self):
        pass


class BinOp(Node):
    """Realiza operações binárias. Contém dois nós filhos"""

    def evaluate(self):
        if self.value == T_PLUS:
            n1, n2 = self.children
            return n1.evaluate() + n2.evaluate()
        if self.value == T_MINUS:
            n1, n2 = self.children
            return n1.evaluate() - n2.evaluate()
        if self.value == T_MULTI:
            n1, n2 = self.children
            return int(n1.evaluate() * n2.evaluate())
        if self.value == T_DIV:
            n1, n2 = self.children
            return int(n1.evaluate() / n2.evaluate())


class UnOp(Node):
    """Realiza operações unárias. Contém um único nó filho"""

    def evaluate(self):
        node = self.children[0]

        if self.value == T_MINUS:
            return -node.evaluate()
        if self.value == T_PLUS:
            return node.evaluate()

        raise OperationError(f"Unexpected value '-'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self):
        return self.value


class NoOp(Node):
    def evaluate(self):
        pass
