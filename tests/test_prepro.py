import pytest
from compiler.errors import SyntaxError
from compiler.prepro import PrePro


class TestPrePro:
    @staticmethod
    def test_valid_comment():
        valid_comment = "this is /* */a valid string"
        expected = "this is a valid string"
        output = PrePro.filter(valid_comment)
        assert output == expected

    @staticmethod
    def test_valid_multiple_comments():
        valid_comment = "this is /* this is a comment */a valid/*another comment */ string"
        expected = "this is a valid string"
        output = PrePro.filter(valid_comment)
        assert output == expected

    @staticmethod
    def test_unclosing_comment():
        valid_comment = "this is /* this is a comment a valid another comment string"
        with pytest.raises(SyntaxError):
            PrePro.filter(valid_comment)
