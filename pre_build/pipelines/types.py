#!/usr/bin/env python3
"""
# [treesource] This controls the types that the variables can take for the compiler
"""


# These are the variable types associated with the signals
class VarType:
    def __init__(
        self,
        bit_size: int,
        signed: bool,
        time_dependent: bool,
        automatic_registers: bool,
        prevent_overflow_underflow: bool,
    ) -> None:
        # Specifies wether to add reg to prevent overflow/underflow
        #   Greatly increase the area
        self._prevent_overflow_underflow = prevent_overflow_underflow

        # The sign of the value (for bit operations use unsigned)
        self._signed = signed

        # The number of registers/bit size for the variable
        assert bit_size > 0
        self._bit_size = bit_size

        # This controls time syncing
        #   This is used to enforce timing requirements in pipelines
        self._time_dependent = time_dependent

        # This will automatically pipeline time dependent values based on hierastics if True
        self._automatic_registers = automatic_registers

        # It does not make sense to have automatic registers while not being time dependent
        if self._automatic_registers and not self._time_dependent:
            raise ValueError(
                f"We cannot add automatic registers when the type is not time dependent, that does not make sense"
            )

    def __eq__(self, other: VarType) -> bool:
        return (
            self._bit_size == other._bit_size
            and self._signed == other._signed
            and self._time_dependent == other._time_dependent
            and self._automatic_registers == other._automatic_registers
            and self._prevent_overflow_underflow == other._prevent_overflow_underflow
        )


# These are the module types for the code to be ran
PYTHON = "python"
MIGEN = "migen"
CALYX = "calyx"
NONE = "None"
ALLOWED_MODULE_TYPES = [PYTHON, MIGEN, CALYX, NONE]


class ModuleType:
    def __init__(self, type: str) -> None:
        # Make sure it is one of the supported types
        assert type in ALLOWED_MODULE_TYPES
        self.type = type

    def __eq__(self, value: ModuleType) -> bool:
        return self.type == value.type
