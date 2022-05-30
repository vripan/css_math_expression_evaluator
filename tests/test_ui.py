import os, sys, unittest
from types import SimpleNamespace

from sympy import EX
import tkinter as tk
from tkinter import messagebox as tk_messagebox

from src.ui import MathExpressionEvaluatorUi
from src.ui_bridge import BackendBridge


import unittest
from unittest.mock import Mock

class UiTest(unittest.TestCase):
    DEFAULT_EXPONENT= "100"
    DEFAULT_RESULT = "70"
    DEFAULT_STEPS = "(a + (b * 20))\n(10 + (b * 20))\n(10 + (3 * 20))\n(10 + 60)\n70\n"
    
    async def _start_app(self):
        self.ui.mainloop()

    def setUp(self):
        self.backend_bridge = BackendBridge()
        self.backend_bridge.exponent = Mock(return_value=UiTest.DEFAULT_EXPONENT)
        self.backend_bridge.compute_data = Mock(return_value=(UiTest.DEFAULT_RESULT, UiTest.DEFAULT_STEPS))

        self.root = tk.Tk()
        self.app = MathExpressionEvaluatorUi(self.root, self.backend_bridge)
        
    def tearDown(self) -> None:
        self.root.destroy()
        
    def __test_field_succes(self, field_callback, expected_value):
        value = field_callback(expected_value)
        self.assertEqual(value, None)
        value = field_callback()
        self.assertEqual(value, expected_value)

    def __test_field_failure(self, field_callback, test_value, exception_type):
        with self.assertRaises(exception_type):
            field_callback(test_value)

    def __get_test_file(self, filename):
        return os.path.join(unittest.test_files_dir, filename)

    def __get_temp_file(self, filename):
        return os.path.join(unittest.temp_files_dir, filename)

    def test_exponent_field(self):
        value = self.app.exponent_value()
        value_int = int(value)
        self.assertGreater(value_int, 0)

        self.__test_field_succes(self.app.exponent_value, "1")
        self.__test_field_succes(self.app.exponent_value, "12")
        self.__test_field_succes(self.app.exponent_value, "10000000")

        self.__test_field_failure(self.app.exponent_value, "0xE12FFE", Exception)
        self.__test_field_failure(self.app.exponent_value, "-12", Exception)
        self.__test_field_failure(self.app.exponent_value, "0", Exception)
        self.__test_field_failure(self.app.exponent_value, "-0", Exception)
        
        self.__test_field_failure(self.app.exponent_value, 1 , Exception)
        self.__test_field_failure(self.app.exponent_value, "" , Exception)
        
    def test_expression_field(self):
        with self.assertRaises(Exception):
            self.app.expression_value()

        self.__test_field_succes(self.app.expression_value, "-100000000")
        self.__test_field_succes(self.app.expression_value, "-1")
        self.__test_field_succes(self.app.expression_value, "0")
        self.__test_field_succes(self.app.expression_value, "1")
        self.__test_field_succes(self.app.expression_value, "100000000")
        
        self.__test_field_succes(self.app.expression_value, "a + b")
        self.__test_field_succes(self.app.expression_value, "X")
        self.__test_field_succes(self.app.expression_value, "abcdef")
        self.__test_field_succes(self.app.expression_value, "a + X * (ce - d) % 2**10 + sqrt(36)")

        self.__test_field_failure(self.app.expression_value, "a, b", Exception)
        self.__test_field_failure(self.app.expression_value, "a##@$$", Exception)

    def test_variables_fields(self):
        self.__test_field_succes(self.app.variables_value, {"a": "1"})
        self.__test_field_succes(self.app.variables_value, {"a": "1231", "c": "221", "d": "1123"})
        self.__test_field_succes(self.app.variables_value, {})
        self.__test_field_succes(self.app.variables_value, {"a": "12111113341231"})
        self.__test_field_succes(self.app.variables_value, {"a": "1", "b": "2", "a": "3"})

        self.__test_field_failure(self.app.variables_value, "a=5", Exception)
        self.__test_field_failure(self.app.variables_value, {"ab": "0"}, Exception)
        self.__test_field_failure(self.app.variables_value, {"a": "0x01"}, Exception)
        self.__test_field_failure(self.app.variables_value, {"a": "-1"}, Exception)
        self.__test_field_failure(self.app.variables_value, {"a": "1", "b": "2", "a": "1", "c":"0xfe"}, Exception)
        self.__test_field_failure(self.app.variables_value, {"a": "1", "b": "2", "a": "1", "#":"###"}, Exception)

    def test_variables_fields_not_unique(self):
        self.app._MathExpressionEvaluatorUi__add_var_fields() 

        for var_box, value_box in self.app.vars.fields:
            var_box.insert(0, "a")
            value_box.insert(0, "1")

        with self.assertRaises(Exception):
            self.app.variables_value()

    def test_steps_fiels(self):
        value = self.app.steps_value()
        self.assertEqual(len(value), 0)

        self.__test_field_succes(self.app.steps_value, "test")
        self.__test_field_succes(self.app.steps_value, "test\ntest")
        self.__test_field_succes(self.app.steps_value, "long_test" * 1000)
        self.__test_field_succes(self.app.steps_value, "")
        self.__test_field_succes(self.app.steps_value, "\b")

    def test_result_field(self):
        with self.assertRaises(Exception):
            self.app.result_value()

        self.__test_field_succes(self.app.result_value, "0")
        self.__test_field_succes(self.app.result_value, "1")
        self.__test_field_succes(self.app.result_value, "1000000")

        self.__test_field_failure(self.app.result_value, "-1000000", Exception)
        self.__test_field_failure(self.app.result_value, "-1", Exception)
        self.__test_field_failure(self.app.result_value, "-0", Exception)

        self.__test_field_failure(self.app.result_value, "a", Exception)
        self.__test_field_failure(self.app.result_value, "X", Exception)
        self.__test_field_failure(self.app.result_value, "##", Exception)
        self.__test_field_failure(self.app.result_value, "-", Exception)
        self.__test_field_failure(self.app.result_value, "+", Exception)
        self.__test_field_failure(self.app.result_value, ")", Exception)

    def test_initial_state(self):
        with self.assertRaises(Exception):
            self.app._MathExpressionEvaluatorUi__command_compute.__undecorated__(self.app)

    def test_load_xml_command(self):
        test_file = self.__get_test_file("test_input_000.xml")
        self.app.open_file_callback = Mock(return_value=SimpleNamespace(name = test_file))
        self.app._MathExpressionEvaluatorUi__command_open_xml_file.__undecorated__(self.app)

        self.assertEqual(self.app.expression_value(), "a + b * 20")
        self.assertEqual(self.app.variables_value(), {"a":"10", "b":"3"})

    def test_load_xml_command_dialog_close(self):
        self.app.open_file_callback = Mock(return_value=None)
        self.app._MathExpressionEvaluatorUi__command_open_xml_file.__undecorated__(self.app)

    def test_run_loaded_xml_file(self):
        test_file = self.__get_test_file("test_input_000.xml")
        expected_result = "70"

        self.app.open_file_callback = Mock(return_value=SimpleNamespace(name = test_file))
        self.app._MathExpressionEvaluatorUi__command_open_xml_file.__undecorated__(self.app)

        self.app._MathExpressionEvaluatorUi__command_compute.__undecorated__(self.app)

        self.assertEqual(self.app.result_value(), expected_result)
        
        steps = self.app.steps_value().split("\n")
        first_step_no_brackets = steps[0].replace(")", "").replace("(", "")
        last_step = steps[-1]
        
        self.assertEqual(first_step_no_brackets, self.app.expression_value())
        self.assertEqual(last_step, expected_result)

    def test_save_as_gui_results(self):
        test_file = self.__get_test_file("test_input_000.xml")
        out_file = self.__get_temp_file("output_000")
        expected_out_file = self.__get_test_file("test_output_000.xml")
        expected_result = "70"

        self.app.open_file_callback = Mock(return_value=SimpleNamespace(name = test_file))
        self.app._MathExpressionEvaluatorUi__command_open_xml_file.__undecorated__(self.app)

        self.app._MathExpressionEvaluatorUi__command_compute.__undecorated__(self.app)

        self.assertEqual(self.app.result_value(), expected_result)
        
        steps = self.app.steps_value().split("\n")
        first_step_no_brackets = steps[0].replace(")", "").replace("(", "")
        last_step = steps[-1]
        
        self.assertEqual(first_step_no_brackets, self.app.expression_value())
        self.assertEqual(last_step, expected_result)

        self.app.save_file_as_callback = Mock(return_value=out_file)
        self.app._MathExpressionEvaluatorUi__command_save_xml_file.__undecorated__(self.app)

        with open(out_file, "rt") as fd_out, open(expected_out_file, "rt") as fd_exp:
            self.assertEqual(fd_out.read(), fd_exp.read())

    def __test_bad_xml(self, filename):
        test_file = self.__get_test_file(filename)
        self.app.open_file_callback = Mock(return_value=SimpleNamespace(name = test_file))
        with self.assertRaises(Exception):
            self.app._MathExpressionEvaluatorUi__command_open_xml_file.__undecorated__(self.app)

    def test_bad_input_xml_001(self, filename="test_input_001.xml"):
        self.__test_bad_xml(filename)

    def test_bad_input_xml_002(self, filename="test_input_002.xml"):
        self.__test_bad_xml(filename)

    def test_bad_input_xml_003(self, filename="test_input_003.xml"):
        self.__test_bad_xml(filename)

    def test_bad_input_xml_004(self, filename="test_input_004.xml"):
        self.__test_bad_xml(filename)