from typing import List

from .errors import OperationError


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children: List[Node] = children

    def evaluate(self):
        pass


class BinOp(Node):
    """Realiza operações binárias. Contém dois nós filhos"""

    def evaluate(self):
        if self.value == '+':
            n1, n2 = self.children
            return n1.evaluate() + n2.evaluate()
        if self.value == '-':
            n1, n2 = self.children
            return n1.evaluate() - n2.evaluate()
        if self.value == '*':
            n1, n2 = self.children
            return n1.evaluate() * n2.evaluate()
        if self.value == '/':
            n1, n2 = self.children
            return n1.evaluate() / n2.evaluate()


class UnOp(Node):
    """Realiza operações unárias. Contém um único nó filho"""

    def evaluate(self):
        if self.value == '-':
            return - self.children[0]
        raise OperationError(f"Unexpected value '-'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self):
        return self.value


class NoOp(Node):
    def evaluate(self):
        pass
