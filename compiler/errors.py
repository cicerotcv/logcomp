from compiler.constants import (E_FUNCTION_ERROR, E_IDENTIFIER_ERROR,
                                E_MISSING_IDENTIFIER, E_OPERATION_ERROR,
                                E_SYNTAX_ERROR, E_TOKEN_ERROR, E_TYPE_ERROR,
                                E_UNCLOSING_DELIMITER)


class Error(Exception):
    def __init__(self, type, description):
        super().__init__(f'{type} :: {description}')


class UnclosingDelimiter(Error):
    def __init__(self, description):
        super().__init__(E_UNCLOSING_DELIMITER, description)


class InvalidToken(Error):
    def __init__(self, description) -> None:
        super().__init__(E_TOKEN_ERROR, description)


class SyntaxError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_SYNTAX_ERROR, description)


class OperationError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_OPERATION_ERROR, description)


class FunctionError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_FUNCTION_ERROR, description)


class MissingIdentifier(Error):
    def __init__(self, description) -> None:
        super().__init__(E_MISSING_IDENTIFIER, description)


class IdentifierError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_IDENTIFIER_ERROR, description)


class TypeError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_TYPE_ERROR, description)
