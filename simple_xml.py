import re
from data_validator import DataValidator

class SimpleXML:
    @staticmethod
    def __extract_data(xml):
        rx_xml = r"<math\s*>[\s\n]*<expression\s*>([\s\S]+?)</expression\s*>[\s\n]*<variables\s*>([\s\S]+?)</variables\s*>[\s\n]*</math\s*>"
        rx_xml_var = r"<var\s+([a-zA-Z_][a-zA-Z0-9_-]*)=\"(\d+)\"/>"
        rx_xml_var_full = r"([\s\n]*<var\s+([a-zA-Z_][a-zA-Z0-9_-]*)=\"(\d+)\"/>[\s\n]*)+"

        matches = re.search(rx_xml, xml)

        if matches is None or len(matches.groups()) != 2:
            raise Exception("invalid XML format")

        expression, raw_vars = matches.groups()
        
        expression = expression.strip(" \n")
        raw_vars = raw_vars.strip("\n ")
        
        DataValidator.is_math_expression(expression)

        full_match = re.fullmatch(rx_xml_var_full, raw_vars)
        if full_match is None:
            raise Exception("invalid XML variables")

        variables_matches = re.findall(rx_xml_var, raw_vars)
        variables = {}
        for match in variables_matches:
            try:
                name, value = match
                DataValidator.is_expression_variable(name)
                DataValidator.is_unsigned_integer(value)

                if name in variables:
                    raise Exception(f"variable name '{name}' not unique")
                variables[name] = value

            except Exception as exc:
                raise Exception(f"invalid variable values: {match}", exc)

        return expression, variables

    @staticmethod
    def load(path):
        expression = ""
        variables = {}

        with open(path, "rt") as fd:
            xml = fd.read()
            expression, variables = SimpleXML.__extract_data(xml)

        return expression, variables

    @staticmethod
    def save(path, expression, variables, result):
        pass
            