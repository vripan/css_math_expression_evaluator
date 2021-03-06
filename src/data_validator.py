import re

class DataValidator:

    @staticmethod
    def is_expression_variable(input_data):
        assert type(input_data) is str, "invalid value type"
        
        rx = r"[a-zA-Z]"
        match = re.fullmatch(rx, input_data)
        if match is None:
            raise Exception("invalid value, expected expression variable, only 'a-zA-Z' allowed")

    @staticmethod
    def is_not_empty(input_data):
        assert type(input_data) is str, "invalid value type"
        
        if len(input_data) == 0:
            raise Exception("invalid value, expected not empty string")

    @staticmethod
    def is_not_zero(input_data):
        assert type(input_data) is str, "invalid value type"
        
        if int(input_data) == 0:
            raise Exception("invalid value, expected non zero value")

    @staticmethod
    def is_unsigned_integer(input_data):
        assert type(input_data) is str, "invalid value type"

        rx = r"\d+"
        match = re.fullmatch(rx, input_data)
        if match is None:
            raise Exception("invalid value, expected unsigned integer")

    @staticmethod
    def is_math_expression(input_data):
        assert type(input_data) is str, "invalid value type"

        for char in input_data:
            if not char.isalnum() and char not in "+-*/()^% ":
                raise Exception("invalid value, expected a valid math expression")
