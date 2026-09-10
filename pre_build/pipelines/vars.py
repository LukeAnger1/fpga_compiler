#!/usr/bin/env python3
"""
# [treesource] These are variables that are used to track the signals and their details
"""

from migen import *  # type: ignore

from pre_build.pipelines.types import VarType
from pre_build.pipelines.module import CustomParentModule


# These are functions that are called within the Var class
#   There are alot of repeat operations that this streamlines for development
def _pre(one: Var, two: Var) -> tuple[Var, Var]:
    """
    Returns one synced, two synced, and the max bit size needed
    """

    # Make sure the types match
    # TODO: Remove the bit size check from here and handle better later
    assert one.type == two.type, (
        f"{one.type} and {two.type} dont match, please manually cast to prevent issues"
    )

    # Add in logic to make sure the signals have the same delay
    one, two = one.sync_delay(two)

    # TODO: Change this logic for bit operations and signed operations, force casting
    # max_bits = max(one.type._bit_size, two.type._bit_size)

    return one, two


def _post(self, result) -> Var:
    pass


# This tracks the names, they all need to be unique
COMPILED_NAME_PREFIX = "compiled_name"

# IMPORTANT TODO: Add in time dominance for non time dependent vars


class Var:
    def __init__(
        self,
        module: CustomParentModule,
        varType: VarType,
        constant_value: None | int = None,
        delay: int = 0,
        name: str | None = None,
    ) -> None:
        # It does not make sense to have a negative delay
        assert delay >= 0
        self._delay = delay

        self.module: CustomParentModule = module

        # Make sure the name is not already taken
        str_name: str = COMPILED_NAME_PREFIX if name is None else name
        self.name = str_name

        assert isinstance(varType, VarType), f"The type is {type(varType)}"
        self.type = varType

        # This is the actual signal representing the variable in hardware
        self._signal = Signal(
            bits_sign=(varType._bit_size, varType._signed), name=str_name
        )
        self.module.builtin_inputs.append(self._signal)  # type: ignore

        # If the variable is set to a constant value nothing can really change about it
        self.constant_value = constant_value
        if constant_value is not None:
            # Constant values should not be time dependent, this adds unnecasry pipelining steps
            assert varType._time_dependent is False

            self.module.comb += self._signal.eq(constant_value)  # type: ignore

    def inc_delay(self) -> Var:
        # Increments the delay and retuns the new variable
        result = type(self)(
            self.module,
            VarType(
                self.type._bit_size,
                self.type._signed,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            None,
            self._delay + 1,
            self.name,
        )
        self.module.sync += result._signal.eq(self._signal)  # type: ignore
        return result

    def sync_delay(self, other: Var) -> tuple[Var, Var]:
        """This function syncs two variables to the same delay, returning the new synced variables in the same order

        Args:
            self (_type_): _description_
        """

        max_delay = max(self._delay, other._delay)

        var1 = self
        var2 = other

        while var1._delay < max_delay:
            var1 = var1.inc_delay()

        while var2._delay < max_delay:
            var2 = var2.inc_delay()

        return var1, var2

    def __abs__(self) -> Var:
        """Overload the absolute value operator for variables

        Returns:
            A new variable representing the absolute value
        """

        # If unsigned, absolute value is just itself
        if not self.type._signed:
            raise ValueError(
                "Why are we taking the absolute vallue of unsigned variable"
            )

        # For signed values, we need to check the sign bit and negate if negative
        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )

        # Check if the value is negative (MSB is 1)
        self.module.comb += If(  # type: ignore
            self._signal[self.type._bit_size - 1],  # Check sign bit # type: ignore
            result._signal.eq(-self._signal),  # Negate if negative # type: ignore
        ).Else(  # type: ignore
            result._signal.eq(self._signal),  # Keep as-is if positive # type: ignore
        )  # type: ignore

        result, _ = result.sync_delay(self)

        return result

    # These are the math operations that are going to be overloaded
    def __add__(self, other: Var) -> Var:
        """Overload the addition operator for variables

        Args:
            other: The other variable to add

        Returns:
            A new variable representing the sum
        """

        # Make sure types match
        self, other = _pre(self, other)

        # TODO: Incremement the max number of bits by 1 if safe overflow

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay + 1,
            name=self.name,
        )
        # self.module.comb += result._signal.eq(self._signal + other._signal)
        # IMPORTANT TODO: Switch to combinational option too
        result.module.sync += result._signal.eq(self._signal + other._signal)  # type: ignore

        return result

    def __sub__(self, other: Var) -> Var:
        """Overload the subtraction operator for variables

        Args:
            other: The other variable to subtract

        Returns:
            A new variable representing the difference
        """

        self, other = _pre(self, other)

        # TODO: Incremement the max number of bits by 1 if safe overflow

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal - other._signal)  # type: ignore

        return result

    def __mul__(self, other: Var | int) -> Var:
        """Overload the multiplication operator for variables

        Args:
            other: The other variable to multiply

        Returns:
            A new variable representing the product
        """

        assert not isinstance(other, int), (
            f"Multiplication by integer is not supported yet, using value {other}"
        )

        assert self.type._signed is False and other.type._signed is False, (
            f"Does not support signed multiplication yet"
        )

        self, other = _pre(self, other)

        # TODO: Double bit size for safe overflow

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal * other._signal)  # type: ignore

        return result

    def __truediv__(self, other: Var) -> Var:
        """Overload the division operator for variables

        Args:
            other: The other variable to divide

        Returns:
            A new variable representing the quotient
        """

        # NOTE: I dont really plan on implementing this right now, division in hardware cane be pipelined and isnt needed at the moment
        # If we do decide to implement it we should do a for loop by the bits for repeat logic then use the operations already defined
        raise NotImplementedError("Division operator is not implemented yet")

    def __eq__(self, other: Var) -> Var:
        """Overload the equality operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal == other._signal)  # type: ignore

        return result

    def __ne__(self, other: Var) -> Var:
        """Overload the inequality operator for variables

        Args:
            other: The other variable to compare to
        """

        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal != other._signal)  # type: ignore

        return result

    def __lt__(self, other: Var) -> Var:
        """Overload the less than operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal < other._signal)  # type: ignore

        return result

    def __le__(self, other: Var) -> Var:
        """Overload the less than or equal to operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal <= other._signal)  # type: ignore

        return result

    def __gt__(self, other: Var) -> Var:
        """Overload the greater than operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal > other._signal)  # type: ignore

        return result

    def __ge__(self, other: Var) -> Var:
        """Overload the greater than or equal to operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            VarType(
                1,
                False,
                self.type._time_dependent,
                self.type._automatic_registers,
                self.type._prevent_overflow_underflow,
                False
            ),
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal >= other._signal)  # type: ignore

        return result

    def __and__(self, other: Var) -> Var:
        """Overload the bitwise AND operator for variables

        Args:
            other: The other variable to AND with

        Returns:
            A new variable representing the bitwise AND result
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal & other._signal)  # type: ignore

        return result

    def __or__(self, other: Var) -> Var:
        """Overload the bitwise OR operator for variables

        Args:
            other: The other variable to OR with

        Returns:
            A new variable representing the bitwise OR result
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal | other._signal)  # type: ignore

        return result

    def __xor__(self, other: Var) -> Var:
        """Overload the bitwise XOR operator for variables

        Args:
            other: The other variable to XOR with

        Returns:
            A new variable representing the bitwise XOR result
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(self._signal ^ other._signal)  # type: ignore

        return result

    def __invert__(self) -> Var:
        """Overload the bitwise NOT operator for variables

        Returns:
            A new variable representing the bitwise NOT result
        """

        result = type(self)(
            self.module,
            self.type,
            constant_value=None,
            delay=self._delay,
            name=self.name,
        )
        self.module.sync += result._signal.eq(~self._signal)  # type: ignore

        return result
