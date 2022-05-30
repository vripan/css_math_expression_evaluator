from typing import List, Tuple
from bignum import BigNum
from expr_parser import ExpressionParser, expr_solve


class BackendBridge:
    def __init__(self):
        pass

    def exponent(self) -> str:
        return str(BigNum.exponent())

    def compute_data(self, expression:str, variables:List[Tuple[str,str]], exponent:int) -> Tuple[str, str]:
        """Bridge method between GUI and backend logic"""
        assert exponent >= 0, "invalid exponent"

        BigNum.exponent(exponent)

        vars = {}
        for var, val in variables:
            vars[var] = BigNum(val)
        parser = ExpressionParser(expression, vars, BigNum)
        expr = parser.run()
        output, result = expr_solve(expr, vars)

        return (str(result), output)
