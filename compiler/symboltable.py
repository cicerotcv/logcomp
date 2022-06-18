from compiler.errors import IdentifierError, TypeError


class SymbolTable:
    def __init__(self, scope_name: str = None):
        self.scope = scope_name
        self._identifiers = {}

    def declare(self, type, identifier):
        self.ensure_not_declared(identifier)
        self._identifiers[identifier] = (type, None)

    def get(self, identifier):
        self.ensure_declared(identifier)
        return self._identifiers[identifier]

    def set(self, identifier, value):
        self.ensure_declared(identifier)
        self.ensure_same_type(identifier, value)
        self._identifiers[identifier] = value

    def ensure_not_declared(self, identifier_name):
        if identifier_name in self._identifiers.keys():
            raise IdentifierError(
                f"Identifier already declared: '{identifier_name}'")

    def ensure_declared(self, identifier_name):
        if identifier_name not in self._identifiers.keys():
            raise IdentifierError(
                f"Identifier not declared: '{identifier_name}'")

    def ensure_same_type(self, identifier_name, value):
        (current_type, _) = self._identifiers.get(identifier_name)
        (new_type, _) = value

        if current_type != new_type:
            raise TypeError(
                f"Expected type '{current_type}' and got '{new_type}'")

    def describe(self):
        print(self._identifiers.keys())


class FuncTable:
    _identifiers = {}

    @staticmethod
    def declare(type, identifier):
        FuncTable.ensure_not_declared(identifier)
        FuncTable._identifiers[identifier] = (type, None)

    @staticmethod
    def get(identifier):
        FuncTable.ensure_declared(identifier)
        return FuncTable._identifiers[identifier]

    @staticmethod
    def set(identifier, value):
        FuncTable.ensure_declared(identifier)
        FuncTable._identifiers[identifier] = value

    @staticmethod
    def ensure_not_declared(identifier_name):
        if identifier_name in FuncTable._identifiers.keys():
            raise IdentifierError("Function already declared")

    @staticmethod
    def ensure_declared(identifier_name):
        if identifier_name not in FuncTable._identifiers.keys():
            raise IdentifierError("Function not declared")

    @staticmethod
    def describe():
        print(FuncTable._identifiers.keys())
