Testing
=======

The testing strategy used to check that the application behaves as expected is **unit testing**. Every component enumerate on :doc:`components<components>` page defines a test suite with multiple test case. Also a coverage report is generated :doc:`here<coverage>`. 

The tesing code is located in the :code:`tests` folder and can be runned using the script :code:`test.py`.

GUI Testing
***********
The component specific test files are :code:`test_ui.py` and :code:`test_ui_bridge.py`. The implemented test cases valides multiple scenarios:

* variables list not unique
* reading and writting GUI fields with valid and invalid values
* initial application state
* invalid and valid XML loading
* open file dialog closed during XML loading
* XML saving
* save file dialog closed during XML saving 
* XML loading, computing and saving 

Expression Parser Testing
*************************

This section contains specifications regarding the Unit Testing conducted for the Expr Parser Component.
Most of the tests use the int class as a substitute for BigNum, in case BigNum does an operation wrong, we can compare it to a flawless implementation, meaning the default int class.

- **test_super_basic**
    Testing a simple operation

- **test_basic**
    Testing multiple basic operations

- **test_special**
    Testing power operators

- **test_parens**
    Testing operations respecting parantheses order

- **test_rem**
    This test checks a remainder operation.

- **test_unknown_token**
    This test check that if we find an unknown character, we indeed get an error.

- **test_missing_paren**
    This test check that if we find a missing paranthese, we indeed get an error.

- **test_sub_negative**
    A negative result should throw an exception.

- **test_div_0**
    This test verifies that division by zero is prevented.

- **test_complex**
    Testing a more complex operation using multiple operators.

- **test_vars**
    Testing variable substitution is done corectly

- **test_sqrt**
    Testing that sqrt operator works

Big Number Testing
***************************
This section contains specifications regarding the Unit Testing conducted for the BigNum Component.

Note: **_MAX_N** represents the maximum range of numbers used in the test methods, which can be modified in the code (defaults to **100**).

    - **test_add_op**
        * Tests the correctness of the Addition operation, by taking a sample of numbers from 0.._MAX_N and adding each one with the rest of the values, comparing the results (as strings) between BigNum additions and integer additions.

    - **test_sub_op**

        * Tests the correctness of the Substraction operation, by taking a sample of numbers from 0.._MAX_N and substracting each one with the rest of the values, comparing the results (as strings) between BigNum substractions and integer substractions.
        * These tests also verify that an Exception is raised by the BigNum class for the values for which we would expect to get a negative result.

    - **test_mul_op**

        * Tests the correctness of the Multiplication operation, by taking a sample of numbers from 0.._MAX_N and multiplying each one with the rest of the values, comparing the results (as strings) between BigNum multiplications and integer multiplications.

    - **test_pow_op**

        * Tests the correctness of the Exponentiation operation, by taking a sample of numbers from 0.._MAX_N and exponentiating each one with the rest of the values, comparing the results (as strings) between BigNum exponentiation and integer exponentiation.

    - **test_mod_op**

        * Tests the correctness of the Modulo operation, by taking a sample of numbers from 0.._MAX_N and calculating the modulo of each one against the rest of the values, comparing the results (as strings) between BigNum modulo and integer modulo.
        * These tests also verify that an Exception is raised by the BigNum class when we would try to calculate modulo 0 of a value.

    - **test_floordiv_op**

        * Tests the correctness of the Floor Division operation, by taking a sample of numbers from 0.._MAX_N and dividing each one with the rest of the values, comparing the results (as strings) between BigNum floor division and integer division.
        * These tests also verify that an Exception is raised by the BigNum class when we would try to divide by 0.

    - **test_sqrt_op**

        * Tests the correctness of the Square Root operation, by taking a sample of numbers from 0.._MAX_N and calculating the square root of each number, comparing the results (as strings) between BigNum sqrt and the floor value of math.sqrt().

    - **test_max_length**

        * Tests that the BigNum class raises an Exception when the maximum digits count is reached, either via an initialization value that is too large, or a value that would result from a computation (i.e. exponentiation).

    - **test_invalid_input**

        * Tests that an Exception is raised when the constructor receives invalid input. For example negative/float numbers, or invalid strings that contain non-digit characters.

    - **test_invalid_cases**

        * Tests than an Exception is raised in every following situation:
            * Division by 0 operation;
            * Substraction that would yield a negative result;
            * Modulo 0 operation;

    - **test_predefined_results**

        * Tests the correctness of operations for which we have a pre-calculated result represented as a string, with which we compare the string representation of the result obtained by using BigNum.