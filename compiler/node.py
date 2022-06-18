from typing import List

from compiler.constants import (LOG_AND, LOG_EQ, LOG_GT, LOG_LT, LOG_OR, OP_CONCAT,
                                OP_DIV, OP_MINUS, OP_MULTI, OP_NOT, OP_PLUS, T_INT, T_STR)
from compiler.errors import OperationError
from compiler.symboltable import SymbolTable
from compiler.nasm import Nasm


class Generator:
    _counter = 0

    @staticmethod
    def get_id():
        # return next(Generator._sequence)
        Generator._counter += 1
        return Generator._counter - 1


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children: List[Node] = children
        self.id = Generator.get_id()

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
        Nasm.put("PUSH EBX;")
        (type2, value2) = n2.evaluate()
        Nasm.put("POP EAX;")

        if self.value == OP_CONCAT:
            # Nasm.put("ADD EAX, EBX")
            Nasm.put(f"MOV EBX, {str(value1) + str(value2)};")
            return (T_STR, str(value1) + str(value2))

        if type1 != type2:
            raise OperationError(
                f"Unexpected operation for types '{type1}' and '{type2}': '{self.value}'")

        if self.value == OP_PLUS:
            Nasm.put("ADD EAX, EBX\t\t; EAX += EBX")
            Nasm.put(f"MOV EBX, EAX\t\t; EBX = EAX")
            return (T_INT, value1 + value2)
        if self.value == OP_MINUS:
            Nasm.put(f"SUB EAX, EBX\t\t; EAX -= EBX")
            Nasm.put(f"MOV EBX, EAX\t\t; EBX = EAX")
            return (T_INT, value1 - value2)
        if self.value == OP_MULTI:
            Nasm.put(f"IMUL EBX\t\t; EAX *= EBX")
            Nasm.put(f"MOV EBX, EAX\t\t; EBX = EAX")
            return (T_INT, value1 * value2)
        if self.value == OP_DIV:
            Nasm.put(f"IDIV EAX, EBX\t\t; EAX /= EBX")
            Nasm.put(f"MOV EBX, EAX\t\t; EBX = EAX")
            return (T_INT, value1 // value2)
        if self.value == LOG_AND:
            return (T_INT, int(value1 and value2))
        if self.value == LOG_OR:
            return (T_INT, int(value1 or value2))
        if self.value == LOG_EQ:
            Nasm.put(f"CMP EAX, EBX;")
            Nasm.put(f"CALL binop_je;")
            return (T_INT, int(value1 == value2))
        if self.value == LOG_GT:
            Nasm.put(f"CMP EAX, EBX;")
            Nasm.put(f"CALL binop_jg;")
            return (T_INT, int(value1 > value2))
        if self.value == LOG_LT:
            Nasm.put(f"CMP EAX, EBX;")
            Nasm.put(f"CALL binop_jl;")
            return (T_INT, int(value1 < value2))

        raise OperationError(f"Unexpected value for BinOp: '{self.value}'")


class UnOp(Node):
    """Realiza operações unárias. Contém um único nó filho"""

    def evaluate(self):
        node = self.children[0]
        (type, value) = node.evaluate()
        Nasm.put("")

        if type != T_INT:
            raise OperationError(
                f"Unexpected unary operator '{self.value}' for type '{type}'")

        if self.value == OP_MINUS:
            Nasm.put(f"MOV EBX, {value};")
            Nasm.put(f"NEG EBX\t\t; EBX = (not) EBX")
            return (T_INT, -value)
        if self.value == OP_PLUS:
            Nasm.put(f"MOV EBX, {value};")
            return (T_INT, value)
        if self.value == OP_NOT:
            Nasm.put(f"MOV EBX, {not value};")
            return (T_INT, int(not value))

        raise OperationError(f"Unexpected value for UnOp: '{self.value}'")


class IntVal(Node):
    """Valor inteiro. Contém um único nó filho"""

    def evaluate(self):
        Nasm.put(f"MOV EBX, {self.value}\t\t; EBX = {self.value}")
        return (T_INT, self.value)


class StrVal(Node):
    """Valor de string. Contém um único nó filho"""

    def evaluate(self):
        # Nasm.put(f"MOV EBX, {self.value};")
        return (T_STR, self.value)


class NoOp(Node):
    def evaluate(self):
        pass


class Identifier(Node):
    def evaluate(self):
        type, value = SymbolTable.get(self.value)
        pos = SymbolTable.pos(self.value)
        Nasm.put(f"MOV EBX, [EBP-{pos}]\t; EBX = {self.value}")
        # MOV EBX, [EBP-"+str(valor) +"]
        return (type, value)


class Assignment(Node):
    def evaluate(self):
        identifier, value = self.children
        assigned_value = value.evaluate()
        SymbolTable.set(identifier.value, assigned_value[0], assigned_value[1])
        pos = SymbolTable.pos(identifier.value)
        Nasm.put(f"MOV [EBP-{pos}], EBX\t; {identifier.value} = EBX")


class Printf(Node):
    def evaluate(self):
        (_, value) = self.children[0].evaluate()
        # print(value)
        Nasm.put("\t\t\t; Print call")
        Nasm.put(f"PUSH EBX;")
        Nasm.put(f"CALL print;")
        Nasm.put(f"POP EBX;\n")


class Scanf(Node):
    def evaluate(self):
        value = int(input())
        Nasm.put(f"MOV EBX, {value};")
        return (T_INT, int(input()))


class VarDec(Node):
    def evaluate(self):
        type = self.value
        for identifier_name in self.children:
            SymbolTable.declare(type, identifier_name)
            Nasm.put(f"PUSH DWORD 0\t; identifier '{identifier_name}' declaration")


class While(Node):
    def evaluate(self):
        condition, routine = self.children

        Nasm.put(f"\nLOOP_{self.id}:\t\t; Begin LOOP_{self.id}\n")
        Nasm.put(f"\t\t\t; LOOP_{self.id} conditions")
        condition.evaluate()

        Nasm.put(f"\nCMP EBX, False;")
        Nasm.put(f"JE EXIT_{self.id};\n")

        Nasm.put(f"\t\t\t; LOOP_{self.id} routine")
        routine.evaluate()

        Nasm.put(f"JMP LOOP_{self.id};")
        Nasm.put(f"EXIT_{self.id}:\n")

        # while evaluation:
        #     routine.evaluate()
        #     (_, evaluation) = condition.evaluate()


class If(Node):
    def evaluate(self):
        Nasm.put(f"IF_{self.id};")

        # if { expression } : { this } else: { that }
        if len(self.children) == 3:
            expression, this, that = self.children

            expression.evaluate()
            Nasm.put(f"CMP EBX, False;")
            Nasm.put(f"JE ELSE_{self.id};")
            this.evaluate()
            Nasm.put(f"ELSE_{self.id};")
            that.evaluate()
            Nasm.put(f"JMP IF_{self.id}_EXIT;")

        # if { expression } : { this }
        elif len(self.children) == 2:
            expression, this = self.children
            expression.evaluate()
            Nasm.put(f"CMP EBX, False;")
            Nasm.put(f"JE IF_{self.id}_EXIT;")
            this.evaluate()

        Nasm.put(f"IF_{self.id}_EXIT:;")

        # if len(self.children) == 3:
        # (_, evaluation) = expression.evaluate()
        #     if (evaluation):
        #         this.evaluate()
        #     else:
        #         that.evaluate()

        # if len(self.children) == 2:
        #     (_, evaluation) = expression.evaluate()
        #     if (evaluation):
        #         this.evaluate()


class Block(Node):
    def evaluate(self):
        for child in self.children:
            child.evaluate()
            Nasm.put("")
