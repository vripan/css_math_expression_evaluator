
from typing import List, Tuple

class BackendBridge:
    def __init__(self):
        pass

    def compute_data(self, expression:str, variables:List[Tuple[str,str]], exponent:int) -> Tuple[str, str]:
        return ("0", "no steps")
