Components
==========

The application is build from multiple components, every one of them with a well defined role. As a generic overview, the first component that user interacts with is the GUI, that reads the input from the fields or from the XML file and then sends it to the expression parsers component that interacts with the big number in order to compute the expression. After the expression is computed the result is returned to the user to be desplayed in GUI or written to file.


GUI Component
*************

The component is responsible with all the I/O operations between the user and the application. There a two ways of interacting with the GUI:

* directly through GUI input fields.
* indirectly through XML files.

More details presented on :doc:`how to run<how_to_run>` page.

.. image:: _static/img/gui_init.png
    :align: center
    :scale: 80%
|

**Backend interaction.** The interaction between backend and the frontend is made using the class :code:`BackendBridge` defined in :code:`ui_bridge.py`, using the two methods available:

* method :code:`exponent(...)` that implements a getter for the internal exponent data field used to populate field :code:`Exponent` on initialization.
* method :code:`compute_data(...)` that calls the needed backend method in order to compute the math expression provided.

**Input validation.** The input is always readed directly from the GUI fields, so there is a uniform way of validating data before sending it to the backend. Because of this, when an XML is loaded, the actual data is first set into the GUI fields in order to be readed leater. The actual data validation is made for every field in the associated setter/getter methods.

**Data constraits.** Every field has some basic constraints in order to verify the input data as follows:

* field **Exponent**: expects a non-zero unsigned integer.
* field **Expression**: expects a non-empty arithmetic expression that contains only the alphanumeric characters and the characters :code:`+-*/()^%`.
* field **Variable Name**: expects a non-empty string of length 1 that matches the character set :code:`[a-zA-Z]`
* field **Variable Value**: expects a unsigned integer smaller the maximum number defined by the exponent.


Expression Parser Component
***************************

.. warning::
    TODO

Big Number Component
********************

This class represents a custom implementation that operates with big numbers, which are stored internally in an array for fast operations.

There is a standard soft limit of 1000 digits per number regarding the output of the operations, but also the intial value attributed to a BigNum instance, which can be modified by the user.

This class implements all basic operations that would be needed in calculating an expression, and can take either an int or a string as input in the constructor.

The internal representation of a BigNum is an array of Base10 digits, stored in reverse order, which help the implemented algorithms for faster calculations without intermediary steps regarding the data representation.

This class is used by the Expression Parser component for evaluating parsed expressions.

**Operations**:
    The following operations are implemented by **BigNum**:

    - **__add__** (Addition):

        * This function performs direct addition of the arrays representation of each instance, which is stored in the internal array of the returned value.
        * This addition is performed value by value of each coresponding index, keeping the carry for the next index addition.

        * **Postcondition**: An assert is used that checks the resulted value is bigger that both inputs.

    - **__sub__** (Substraction):

        * This function performs direct substraction of the arrays representation of each instance, which is stored in the internal array of the returned value.
        * This substraction is performed value by value of each coresponding index, while also taking into acount a remainder, which is substracted from the next index substraction value.

        * **Precondition**: An exception is thrown if the substracted value is bigger than the value from which it's being substracted, which would yield a negative result, which is not supported.
        * **Postcondition**: An assert is used that checks the resulted value is smaller or equal than the initial value.

    - **__mul__** (Multiplication):

        * This function performs direct multiplication of the 2 internal arrays, which is stored in the internal array of the returned value.
        * This multiplication is performed via a double for loop, in which each value in the array of the first element is multiplied by every value in the second, which is then added to the coresponding index value in the result array, with the carry being added over to the next one.

        * **Postcondition**: An assert is used that checks that at least one of the values is less or equal than the result.

    - **__pow__** (Power):

        * For this operation, we used a recursive method of an algorithm known as exponentiation by squaring, which takes advantage of the BigNum representation for calculations in this case.
        * In this algorithm, the basic idea is to square the first operand, and divide the power by 2, which we recursively pass as arguments to the function that returns the calculated value.

        * **Postcondition**: An assert is used to validate that the result is bigger than the first operand, excepting a power of 0 or 1.

    - **__mod__** (Modulo):

        * For this operation, we used a simple mathematic formula to calculate the modulo of the operands, by using substraction, division and multiplication operations, while taking advantage of the BigNum representation and implemented operations.

        * **Precondition**: An exception is thrown if the modulus is not bigger than 0.
        * **Postcondition**: An assert is used to validate that the result (remainder) is less than the modulus operand.

    - **__floordiv__** (Floor/Integer Division):

        * For this operation, we implemented an algorithm that calculates integer division with remainder.
        * In this algorithm, we divide the values via multiple repeated substractions at each step, which finally leaves us with a remainder, and the quotient, which is the returned value.

        * **Precondition**: An exception is thrown if the divisor is 0.
        * **Postcondition**: An assert is used to verify that the result is correct, by validating that the quotient multiplied by the divisor plus the remainder is equal to the dividend.

    - **sqrt** (Square Root):

        * For this operation, we implemented an algorithm that calculates square root by long division.
        * This algorithm involves a series of multiple steps that calculate the square root digit-by-digit, by taking advantage of the decimal place value system. (`reference <https://www.cantorsparadise.com/the-square-root-algorithm-f97ab5c29d6d>`_)
        * For this algorithm we also implemented a binary search method for fast calculation of the square root used on 2 digit numbers, used at the start of this algorithm.
        * The returned value of this operation is an integer aproximation of the result, since we only work with integers.

        * **Postcondition**: An assert is used to validate that the result squared is less or equal than the input, and that (result + 1) squared is strictly bigger than the input.

**Other Methods**:
    - **__str__** (String Representation)

        * This method returns the string representation of the number, in Base10.

    - **exponent**

        * This is a class method used to set/get the maxium digits limit.