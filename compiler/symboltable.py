from typing import Dict
from compiler.errors import IdentifierError, TypeError

class Identifier:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos

    def update(self, value):
        self.value = value

    def validate(self, type):
        if not self.type == type:
            raise TypeError(f"Expected type '{self.type}' and got '{type}'")


    def tuple(self):
        return (self.type, self.value)


class SymbolTable:
    _identifiers:Dict[str, Identifier] = {}
    ebp = 4

    @staticmethod
    def declare(type, identifier):
        SymbolTable.ensure_not_declared(identifier)
        SymbolTable._identifiers[identifier] = Identifier(type, None, SymbolTable.ebp)
        SymbolTable.ebp += 4

    @staticmethod
    def get(identifier):
        """(type, current_value, stack_position)"""
        SymbolTable.ensure_declared(identifier)
        return SymbolTable._identifiers[identifier].tuple()

    @staticmethod
    def pos(identifier_name):
        SymbolTable.ensure_declared(identifier_name)
        return SymbolTable._identifiers[identifier_name].pos

    @staticmethod
    def set(identifier, type, value):
        SymbolTable.ensure_declared(identifier)
        SymbolTable._identifiers[identifier].validate(type)
        SymbolTable._identifiers[identifier].update(value)

    @staticmethod
    def ensure_not_declared(identifier_name):
        if identifier_name in SymbolTable._identifiers.keys():
            raise IdentifierError("Identifier already declared")

    @staticmethod
    def ensure_declared(identifier_name):
        if identifier_name not in SymbolTable._identifiers.keys():
            raise IdentifierError("Identifier not declared")


    @staticmethod
    def describe():
        print(SymbolTable._identifiers)
