import unittest, os, shutil, sys

# path hack to be able to run test.py as main
root_dir =  os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
src_dir = os.path.join(root_dir, "src")
sys.path.insert(0, src_dir)
sys.path.insert(0, root_dir)

from test_ui import *
from test_bignum import *
from test_expr_parser import *
from test_ui_bridge import *

if __name__ == "__main__":
    unittest.test_files_dir = os.path.join(root_dir, "resources")
    unittest.temp_files_dir = os.path.join(root_dir, ".temp")

    if os.path.exists(unittest.temp_files_dir):
        shutil.rmtree(unittest.temp_files_dir)
    os.mkdir(unittest.temp_files_dir)

    unittest.main()