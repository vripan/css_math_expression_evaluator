import unittest, os, shutil

from test_ui import *
from test_bignum import *
from test_expr_parser import *
from test_ui_bridge import *

if __name__ == "__main__":
    unittest.test_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    unittest.temp_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".temp")

    if os.path.exists(unittest.temp_files_dir):
        shutil.rmtree(unittest.temp_files_dir)
    os.mkdir(unittest.temp_files_dir)

    unittest.main()