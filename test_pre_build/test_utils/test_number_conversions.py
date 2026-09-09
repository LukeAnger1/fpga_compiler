#!/usr/bin/env python3
"""
This is a file that contains utility functions for the project
# [treesource] This is a file that contains utility functions for the project
"""

from pre_build.utils.number_conversions import UnsignedRegValue, SignedRegValue


def test_data_preservation():
    # This is a test to make sure all data types preserve their data
    initial_value = 3
    bit_size = 4

    reg_value = UnsignedRegValue(initial_value, bit_size)
    assert initial_value == reg_value.get_python_rep()

    reg_value = SignedRegValue(initial_value, bit_size)
    assert initial_value == reg_value.get_python_rep()

    # Test the negative version
    initial_value = -3
    reg_value = SignedRegValue(initial_value, bit_size)
    assert initial_value == reg_value.get_python_rep()


if __name__ == "__main__":
    test_data_preservation()
    print(f"tests passed {__file__}")
