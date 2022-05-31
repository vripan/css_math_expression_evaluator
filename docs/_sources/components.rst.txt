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

.. warning::
    TODO
