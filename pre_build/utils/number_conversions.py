#!/usr/bin/env python3
"""
This is a file that contains utility functions for the project
# [treesource] This is a file that contains utility functions for the project
"""

import math


# This represents the register value of the python numbers
class RegValue:
    def __init__(self, value: int | float, bit_size: int) -> None:

        # We need to have at least one bit for this to make sense
        assert bit_size > 0

        # We want to have enough bits to represent, this is checked in children

        # Set in the children
        self._internal_rep = -1

    def get_internal(self) -> int:
        return self._internal_rep


class UnsignedRegValue(RegValue):
    def __init__(self, value: int, bit_size: int) -> None:
        super().__init__(value, bit_size)

        # Make sure the value is non negative as it is unsigned
        assert value >= 0
        assert isinstance(value, int)

        # Make sure we have enough bits to represent the number
        needed_bits = get_needed_bits_to_represent_unsigned(value)
        assert bit_size >= needed_bits

        # Do the internal save as an int, this is messy. I dont want to make this rep public, use function
        self._internal_rep = _convert_positive_int_to_bits(value, bit_size)
        self.bit_size = bit_size

    def get_python_rep(self) -> int:
        return _convert_bits_to_positive_int(self._internal_rep, self.bit_size)


class SignedRegValue(RegValue):
    def __init__(self, value: int, bit_size: int) -> None:
        super().__init__(value, bit_size)

        assert isinstance(value, int)

        # Make sure we have enough bits to represent the number
        needed_bits = get_needed_bits_to_represent_signed(value)
        assert bit_size >= needed_bits

        # Do the internal save as an int, this is messy. I dont want to make this rep public, use function
        self._internal_rep = _convert_int_to_bits(value, bit_size)
        self.bit_size = bit_size

    def get_python_rep(self) -> int:
        return _convert_bits_to_int(self._internal_rep, self.bit_size)


def get_needed_bits_to_represent_unsigned(value: int):
    return math.floor(math.log2(value)) + 1


def get_needed_bits_to_represent_signed(value: int) -> int:
    is_neg = 1 if value < 0 else 0
    return math.floor(math.log2(abs(value) + is_neg)) + 2


def _convert_bits_to_int(value_bit: int, num_bits: int) -> int:
    """Convert a 2s complement representation to an integer."""
    assert isinstance(value_bit, int), "Input must be an integer"
    assert isinstance(num_bits, int), "Number of bits must be an integer"
    assert num_bits > 0, "Number of bits must be positive"

    if value_bit & (1 << (num_bits - 1)):
        return value_bit - (1 << num_bits)
    else:
        return value_bit


def _convert_int_to_bits(value_int: int, num_bits: int) -> int:
    """Convert an integer to a 2s compliment representation."""
    assert isinstance(value_int, int), "Input must be an integer"
    assert isinstance(num_bits, int), "Number of bits must be an integer"
    assert num_bits > 0, "Number of bits must be positive"

    return value_int & ((1 << num_bits) - 1)


def _convert_bits_to_positive_int(value_bit: int, num_bits: int) -> int:
    """Convert a bit representation to a positive integer."""
    assert isinstance(value_bit, int), "Input must be an integer"
    assert isinstance(num_bits, int), "Number of bits must be an integer"
    assert num_bits > 0, "Number of bits must be positive"

    return value_bit & ((1 << num_bits) - 1)


def _convert_positive_int_to_bits(value_int: int, num_bits: int) -> int:
    """Convert a positive integer to a bit representation."""
    assert isinstance(value_int, int), "Input must be an integer"
    assert isinstance(num_bits, int), "Number of bits must be an integer"
    assert num_bits > 0, "Number of bits must be positive"
    assert value_int >= 0, "Input integer must be non-negative"

    return value_int & ((1 << num_bits) - 1)
