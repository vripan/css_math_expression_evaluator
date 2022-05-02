
from typing import List, Tuple
from bignum import BigNum
class BackendBridge:
    def __init__(self):
        pass

    def compute_data(self, expression:str, variables:List[Tuple[str,str]], exponent:int) -> Tuple[str, List[str]]:
        """Bridge method between GUI and backend logic"""

        BigNum.exponent(exponent)

        return ("0", ["no steps"])
