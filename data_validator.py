import re

class DataValidator:

    @staticmethod
    def is_expression_variable(input_data):
        if type(input_data) != str:
            return

        rx = r"[a-zA-Z]"
        match = re.fullmatch(rx, input_data)
        if match is None:
            raise Exception("invalid value, expected expression variable")


    @staticmethod
    def is_unsigned_integer(input_data):
        rx = r"\d+"
        match = re.fullmatch(rx, input_data)
        if match is None:
            raise Exception("invalid value, expected unsigned integer")

    @staticmethod
    def is_math_expression(input_data):
        pass