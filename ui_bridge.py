
from typing import List, Tuple
from bignum import BigNum
class BackendBridge:
    def __init__(self):
        pass

    def exponent(self) -> str:
        return str(BigNum.exponent())

    def compute_data(self, expression:str, variables:List[Tuple[str,str]], exponent:int) -> Tuple[str, str]:
        """Bridge method between GUI and backend logic"""

        BigNum.exponent(exponent)

        return ("0", "no steps")
