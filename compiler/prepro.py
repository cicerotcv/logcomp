from compiler.errors import SyntaxError


class PrePro:
    @staticmethod
    def filter(expression):
        start = expression.find('/*')

        if start == -1:
            return expression

        end = expression.find('*/')

        if end == -1:
            raise SyntaxError("Comment block doesn't close")

        replace_string = expression[start:end + 2]
        expression = expression.replace(replace_string, '', 1)

        return PrePro.filter(expression)
