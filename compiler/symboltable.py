class SymbolTable:
    _identifiers = {}

    @staticmethod
    def get(identifier):
        if identifier not in SymbolTable._identifiers:
            raise Exception(":D")

        return SymbolTable._identifiers[identifier]

    @staticmethod
    def set(identifier, value):
        SymbolTable._identifiers[identifier] = value

    @staticmethod
    def describe():
        print(SymbolTable._identifiers)
