#!/usr/bin/env python3
"""
# [treesource] This is a class that generates a module with multiple clock
"""

from migen import *

from pre_build.pipelines.types import (
    VarType,
    ModuleType,
    MIGEN,
    MULTI,
)
from pre_build.pipelines.module_implementation.parent import CustomParentModule
from pre_build.pipelines.module_implementation.migen import MigenPipelineCompiler


class MultiClockPipelineCompiler(CustomParentModule):
    type = ModuleType(MULTI)

    def __init__(self, module_name: str, sub_module_type: str = MIGEN) -> None:
        # A new module of the choosen type is built whenever a new clock is added in
        self.sub_module_type = ModuleType(sub_module_type)

        # This dictionary maps the register widths with the corresponding modules
        self.register_width_mapping: dict[int, CustomParentModule] = dict()

        self.__module__ = module_name

    def get_module_from_register_width(self, register_width: int):
        # If already constructed return
        if register_width in self.register_width_mapping:
            return self.register_width_mapping[register_width]

        # Construct the module based on the sub module type
        created_sub_module = None
        if self.sub_module_type == ModuleType(MIGEN):
            created_sub_module = MigenPipelineCompiler(
                f"{self.__module__}_{register_width}"
            )
        else:
            raise ValueError(f"Only support migen as sub module atm")

        # Construt new module for the new clock
        self.register_width_mapping[register_width] = created_sub_module
        return self.register_width_mapping[register_width]

    def register_signal(self, signal: Signal, varType: VarType):
        module = self.get_module_from_register_width(varType._register_width)
        module.register_signal(signal, varType)

    def sync_wrapper(self, statement, varType: VarType):
        module = self.get_module_from_register_width(varType._register_width)
        module.sync_wrapper(statement, varType)

    def comb_wrapper(self, statement, varType: VarType):
        module = self.get_module_from_register_width(varType._register_width)
        module.comb_wrapper(statement, varType)

    def sync_comb_wrapper(self, statement, varType: VarType):
        module = self.get_module_from_register_width(varType._register_width)
        module.sync_comb_wrapper(statement, varType)

    def compile(
        self, output_dir: str = "hdl/compiled_pipelines", output_vars: list["Var"] = []
    ) -> dict[int, int]:
        """Compile a module for each clock, returns the delay of each keyed by register width"""

        # Split the outputs to the module of their clock
        outputs_by_width: dict[int, list["Var"]] = dict()
        for output in output_vars:
            outputs_by_width.setdefault(output.type._register_width, []).append(output)

        # Make sure every clock with an output has a module
        for register_width in outputs_by_width:
            self.get_module_from_register_width(register_width)

        # Compile all the modules in the values
        # TODO: Wire the modules together
        delays: dict[int, int] = dict()
        for register_width, module in self.register_width_mapping.items():
            delays[register_width] = module.compile(
                output_dir, outputs_by_width.get(register_width, [])
            )
        return delays
