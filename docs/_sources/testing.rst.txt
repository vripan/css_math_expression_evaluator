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

Big Number Testing
***************************
