#!/usr/bin/env python3
"""
# [treesource] This is the module class that can be converted to verilog module amongst other things
"""

from migen import *
from migen.fhdl import verilog

from pre_build.utils.file_operations import save_file
from pre_build.pipelines.types import VarType, ModuleType, NONE


# This is the parent class
#   When making a new backend, make a child of this class
class CustomParentModule:
    type = ModuleType(NONE)
    unique_name_tracker: set[str] = set()
