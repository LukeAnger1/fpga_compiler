#!/usr/bin/env python3
"""
# [treesource] Test to generate a define file
"""

from pre_build.macros.macros_generator import generate_define_file


def test_generate_file():

    # Dictionary that will be generated
    defines: dict[str, (str | int)] = dict()
    defines["test1"] = 1
    defines["test2"] = 2
    defines["test3"] = 3

    generate_define_file(defines, "hdl/tests_dont_use", "test_defines")


if __name__ == "__main__":
    test_generate_file()
    print(f"tests passed {__file__}")
