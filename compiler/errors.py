# errors
E_TOKEN_ERROR = 'invalid_token'
E_SYNTAX_ERROR = 'syntax_error'
E_OPERATION_ERROR = 'operation_error'
E_MISSING_IDENTIFIER = 'missing_identifier'


class Error(Exception):
    def __init__(self, type, description):
        super().__init__(f'{type} :: {description}')


class InvalidToken(Error):
    def __init__(self, description) -> None:
        super().__init__(E_TOKEN_ERROR, description)


class SyntaxError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_SYNTAX_ERROR, description)


class OperationError(Error):
    def __init__(self, description) -> None:
        super().__init__(E_SYNTAX_ERROR, description)


class MissingIdentifier(Error):
    def __init__(self, description) -> None:
        super().__init__(E_MISSING_IDENTIFIER, description)
