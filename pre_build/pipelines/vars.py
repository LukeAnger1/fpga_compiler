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

    assert one.type._prevent_overflow_underflow is False, (
        f"Currently not supporting the overflow/underflow safety"
    )

    # Make sure the types match
    # NOTE: The bit size is going to be fixed by extending the bits to allow logic to work
    # assert one.type._bit_size == two.type._bit_size
    assert one.type._signed == two.type._signed
    # NOTE: The time dependent check does not matter, there is logic lower to maintain time dependence
    # assert one.type._time_dependent == two.type._time_dependent
    assert one.type._automatic_registers == two.type._automatic_registers
    assert one.type._prevent_overflow_underflow == two.type._prevent_overflow_underflow
    assert one.type._enforce_same_bit_sizes == two.type._enforce_same_bit_sizes

    # Add in logic to make sure the signals have the same delay
    one, two = one.sync_delay(two)

    # Sync size, this is only done if both numbers are signed
    #   This is because we need to account for the 1s that cause the flipage
    #   As of now I think positive numbers are fine

    # Case where the bit sizes are the same
    if one.type._bit_size == two.type._bit_size:
        return one, two

    # They have different bit sizes so if either one is type enforced we need to throw error
    if one.type._enforce_same_bit_sizes or two.type._enforce_same_bit_sizes:
        raise ValueError(f"The variables do not have the same size")

    # Find the lower bit sizes
    if one.type._bit_size < two.type._bit_size:
        return one.extend(two.type._bit_size), two

    return one, two.extend(one.type._bit_size)


# Fatory functions to generate new var types
#   This is used specifically for the dunder operations
def construct_new_var_n_size(self: Var) -> Var:
    return construct_new_var_n_set_size(self, self.type._bit_size)


def construct_new_var_n_set_size(self: Var, new_size: int) -> Var:
    # The new delay is calculated
    if self.type._automatic_registers:
        # Safely save in the registers
        new_delay = self._delay + 1
    else:
        new_delay = self._delay

    result = type(self)(
        self.module,
        VarType(
            new_size,
            self.type._signed,
            self.type._time_dependent,
            self.type._automatic_registers,
            self.type._prevent_overflow_underflow,
            self.type._enforce_same_bit_sizes,
        ),
        constant_value=None,
        delay=new_delay,
        name=self.name,
    )
    return result


def construct_new_var_1_size(self: Var) -> Var:
    # The new delay is calculated
    if self.type._automatic_registers:
        # Safely save in the registers
        new_delay = self._delay + 1
    else:
        new_delay = self._delay

    result = type(self)(
        self.module,
        VarType(
            1,
            False,
            self.type._time_dependent,
            self.type._automatic_registers,
            self.type._prevent_overflow_underflow,
            False,
        ),
        constant_value=None,
        delay=new_delay,
        name=self.name,
    )
    return result


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

            # IMPORTANT TODO: Change this to the internal rep class I made
            self.module.comb += self._signal.eq(constant_value)  # type: ignore

    def extend(self, new_bit_size: int) -> Var:
        """
        This is a function to add more bits to the bit size
        """

        assert new_bit_size > self.type._bit_size, (
            f"cannot extend to a bit size that is not bigger"
        )

        # The construct builder will keep the same signness so should be fine there
        result = construct_new_var_n_set_size(self, new_bit_size)
        old_bit_size = self.type._bit_size

        if self.type._signed:
            # Extend with 1s if the last digit is a 1 to preserve the sign
            statement = If(  # type: ignore
                self._signal[self.type._bit_size - 1],  # Check sign bit # type: ignore
                result._signal.eq(
                    Cat(
                        self._signal,
                        Replicate(Constant(1, 1), new_bit_size - old_bit_size),
                    )
                ),  # Negate if negative # type: ignore
            ).Else(  # type: ignore
                result._signal.eq(
                    Cat(
                        self._signal,
                        Replicate(Constant(0, 1), new_bit_size - old_bit_size),
                    )
                ),  # Keep as-is if positive # type: ignore
            )  # type: ignore
        else:
            # Extend with 0s
            statement = result._signal.eq(
                Cat(
                    self._signal, Replicate(Constant(0, 1), new_bit_size - old_bit_size)
                )
            )

        # Automatic or not
        if self.type._automatic_registers:
            self.module.sync += statement
        else:
            self.module.comb += statement

        return result

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
                False,
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

        # If there is no time dependence they are synced, return same
        if self.type._time_dependent is False and other.type._time_dependent is False:
            return self, other

        # If there is one that is time dependent then the delay is the max delay
        if self.type._time_dependent is False:
            max_delay = other._delay
        elif other.type._time_dependent is False:
            max_delay = self._delay
        else:
            # They are both time dependent so sync to the slowest
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
        result = construct_new_var_n_size(self)

        # Check if the value is negative (MSB is 1)
        if self.type._automatic_registers:
            self.module.sync += If(  # type: ignore
                self._signal[self.type._bit_size - 1],  # Check sign bit # type: ignore
                result._signal.eq(-self._signal),  # Negate if negative # type: ignore
            ).Else(  # type: ignore
                result._signal.eq(
                    self._signal
                ),  # Keep as-is if positive # type: ignore
            )  # type: ignore
        else:
            self.module.comb += If(  # type: ignore
                self._signal[self.type._bit_size - 1],  # Check sign bit # type: ignore
                result._signal.eq(-self._signal),  # Negate if negative # type: ignore
            ).Else(  # type: ignore
                result._signal.eq(
                    self._signal
                ),  # Keep as-is if positive # type: ignore
            )  # type: ignore

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

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            result.module.sync += result._signal.eq(self._signal + other._signal)  # type: ignore
        else:
            result.module.comb += result._signal.eq(self._signal + other._signal)  # type: ignore

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

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal - other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal - other._signal)  # type: ignore

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

        self, other = _pre(self, other)

        # TODO: Double bit size for safe overflow

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal * other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal * other._signal)  # type: ignore

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

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal == other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal == other._signal)  # type: ignore

        return result

    def __ne__(self, other: Var) -> Var:
        """Overload the inequality operator for variables

        Args:
            other: The other variable to compare to
        """

        self, other = _pre(self, other)

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal != other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal != other._signal)  # type: ignore

        return result

    def __lt__(self, other: Var) -> Var:
        """Overload the less than operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal < other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal < other._signal)  # type: ignore

        return result

    def __le__(self, other: Var) -> Var:
        """Overload the less than or equal to operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal <= other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal <= other._signal)  # type: ignore

        return result

    def __gt__(self, other: Var) -> Var:
        """Overload the greater than operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal > other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal > other._signal)  # type: ignore

        return result

    def __ge__(self, other: Var) -> Var:
        """Overload the greater than or equal to operator for variables

        Args:
            other: The other variable to compare to
        """

        # Add in logic to make sure the signals have the same delay
        self, other = _pre(self, other)

        result = construct_new_var_1_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal >= other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal >= other._signal)  # type: ignore

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

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal & other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal & other._signal)  # type: ignore

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

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal | other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal | other._signal)  # type: ignore

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

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(self._signal ^ other._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(self._signal ^ other._signal)  # type: ignore

        return result

    def __invert__(self) -> Var:
        """Overload the bitwise NOT operator for variables

        Returns:
            A new variable representing the bitwise NOT result
        """

        result = construct_new_var_n_size(self)

        if self.type._automatic_registers:
            self.module.sync += result._signal.eq(~self._signal)  # type: ignore
        else:
            self.module.comb += result._signal.eq(~self._signal)  # type: ignore

        return result
