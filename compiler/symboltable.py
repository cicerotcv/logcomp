from compiler.errors import IdentifierError, TypeError


class SymbolTable:
    _identifiers = {}

    @staticmethod
    def declare(type, identifier):
        SymbolTable.ensure_not_declared(identifier)
        SymbolTable._identifiers[identifier] = (type, None)

    @staticmethod
    def get(identifier):
        SymbolTable.ensure_declared(identifier)
        return SymbolTable._identifiers[identifier]

    @staticmethod
    def set(identifier, value):
        SymbolTable.ensure_declared(identifier)
        SymbolTable.ensure_same_type(identifier, value)
        SymbolTable._identifiers[identifier] = value

    @staticmethod
    def ensure_not_declared(identifier_name):
        if identifier_name in SymbolTable._identifiers.keys():
            raise IdentifierError("Identifier already declared")

    @staticmethod
    def ensure_declared(identifier_name):
        if identifier_name not in SymbolTable._identifiers.keys():
            raise IdentifierError("Identifier not declared")

    @staticmethod
    def ensure_same_type(identifier_name, value):
        (current_type, _) = SymbolTable._identifiers.get(identifier_name)
        (new_type, _) = value

        if current_type != new_type:
            raise TypeError(
                f"Expected type '{current_type}' and got '{new_type}'")

    @staticmethod
    def describe():
        print(SymbolTable._identifiers)
