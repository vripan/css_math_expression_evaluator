Assertions
==========

Every application component checks preconditions, invariants and postconditions.

GUI
***
The application user interfaces treats the majority of cases as exceptions. The relevant preconditions in GUI are related to string validations because all getters and setters use expects string as argument type:

* **parameter type** checks, e.g. :code:`assert type(param) is str`
* **parameter len** checks, e.g. :code:`assert len(result) > 0`

Expression Parser
*****************

Preconditions:

I. Solver
    **tokenize()**:
    - cannot call tokenize() more times

II. Parser
    
    **__init__()**:
    - check for required operations on big_number_type: __add__, __sub__, __mul__, __floor, __mod__, __pow__
    - expression cannot be empty

    **peek()**:
    - method cannot be called when there is no token left in stream

    **eat()**:
    - method cannot be called when there is no token left in stream
    
III. Solver
    **solve_normal()**:
    - we assert that the type we get from solving partial expressions is the same type as the one expected

* assertions were also used throughout the code to check for unreachable code execution(unexpected switch cases, etc)

Big Number
**********
The following operations contain pre/post conditions checks:

- **__add__** (Addition):
    * **Postcondition**: An assert is used that checks the resulted value is bigger that both inputs.

- **__sub__** (Substraction):
    * **Precondition**: An exception is thrown if the substracted value is bigger than the value from which it's being substracted, which would yield a negative result, which is not supported.
    * **Postcondition**: An assert is used that checks the resulted value is smaller or equal than the initial value.

- **__mul__** (Multiplication):
    * **Postcondition**: An assert is used that checks that at least one of the values is less or equal than the result.

- **__pow__** (Power):
    * **Postcondition**: An assert is used to validate that the result is bigger than the first operand, excepting a power of 0 or 1.

- **__mod__** (Modulo):
    * **Precondition**: An exception is thrown if the modulus is not bigger than 0.
    * **Postcondition**: An assert is used to validate that the result (remainder) is less than the modulus operand.

- **__floordiv__** (Floor/Integer Division):
    * **Precondition**: An exception is thrown if the divisor is 0.
    * **Postcondition**: An assert is used to verify that the result is correct, by validating that the quotient multiplied by the divisor plus the remainder is equal to the dividend.

- **sqrt** (Square Root):
    * **Postcondition**: An assert is used to validate that the result squared is less or equal than the input, and that (result + 1) squared is strictly bigger than the input.
