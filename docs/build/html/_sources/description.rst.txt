Project description
===================
Accessed on May 30, 2022.

Software Quality - Project
==========================
Goal
----

Develop an application which allows carrying out operations with very big numbers (positive integers).

Phase 1 - application development
---------------------------------

Specifications
**************

* The numbers are stored as arrays; a way of controlling the number size must be provided.
* Basic operations to be implemented: addition, subtraction, multiplication, division (integer), power, square root.
* User interface

    * The user requests the computation of an arithmetic expression (e.g., (a + b) * a) and provides the values of the variables.
    * The program displays the results of each step in the computation. Any incorrect outcome (negative result of a subtraction, division by 0) must be signaled explicitly, which results in immediately terminating the computation.
    * Interactive mode: the expression and the values of the variables are entered through a user dialog, which allows creating the expression as a composition of basic operations. The results are also displayed in the same dialog window.
    * Automatic mode: the data input is read from an XML file. Also, the results are written into an XML file.
  
The implementation must not make use of library functions, i.e., the code must be written by the programmers.

Permanent communication with the beneficiary is necessary, so feel free to ask any questions you may have about the requirements. Programs that do not do what they are supposed to, due to misunderstanding the requirements, will be penalized.

Any programming language may be used, provided there are unit testing and mocking tools for it, as well as assertions (which must be language-specific, apart from unit testing assertions); all these will be necessary during the next phases.

It is recommended to design a program structure as simple as possible, without including any additional features than the ones mentioned above. The goal is to create a working version of the program, not necessarily fully stable or error-free, on which testing techniques will subsequently be applied.

Throughout the project phases it is also necessary to write the documentation, which will be delivered in the final phase.

Deadlines
*********

* Set up the teams (3-4 persons): April 19
* Finalize the program development: May 3

Phase 2 - unit testing
----------------------

Specifications
**************

* Use of unit testing tools to test the code developed during phase 1.
* Reminder: unit testing is about discovering if the module being tested can handle incorrect input data (provided by other modules or by application I/O). Error fixing is NOT required.
* Testing must provide code coverage as complete as possible. For indications regarding the conditions to be tested, read the courses.
* Each module must be tested independently. For simulating the interactions with other modules, where necessary, mocking will be used.
  
Deadline
********

* Finalize the unit testing code: May 17

Phase 3 - use of assertions
---------------------------

Specifications
**************

* Assertions will be inserted in the application code, in order to check the preconditions, postconditions, and invariants for the operations implemented during phase 1. The assertions are inserted directly into the application code, so this phase has nothing to do with unit testing.
* If the programming used for development has no built-in assertions, a function/method must be written to provide similar behaviour.
  
Deadline
********

* Finalize the assertions code: May 24

Phase 4 - documentation
-----------------------

Specifications
**************

* Write the documentation for phases 1-3.
* There is no specific requirement for the size of the documentation, but everything that has been done must be described clearly.
* The contribution of each team member must be stated explicitly.
  
Deadline
********

* The documentation will be discussed on May 31.