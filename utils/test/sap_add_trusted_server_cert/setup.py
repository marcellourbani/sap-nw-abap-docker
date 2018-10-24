"""Initializes PYTHONPATH to make find modules from the utils dir"""

import os
import sys
import imp


def init():
    sys.path.insert(0, './mock')


def import_utils_executable(exe_name):
    """Imports an executable from the project diretory utils"""

    exe_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', exe_name)
    sys.modules[exe_name] = module = imp.load_source(exe_name, exe_path)

    return module
