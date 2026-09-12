#!/usr/bin/env python3
"""
# [treesource] This is the module class that can be converted to verilog module amongst other things using migen
"""

from migen import *
from migen.fhdl import verilog

from pre_build.utils.file_operations import save_file
from pre_build.pipelines.types import VarType, ModuleType, NONE, PYTHON, CALYX, MIGEN
from pre_build.macros.macros_generator import generate_define_file
from pre_build.macros.runtime_python_generator import generate_python_file
from pre_build.pipelines.module_implementation.parent import CustomParentModule


class MigenPipelineCompiler(CustomParentModule, Module):
    type = ModuleType(MIGEN)

    def __init__(self, module_name: str):
        # TODO: Add in logic to add in valid signal for tracking
        #         Add in logic for stall and ready

        # This is sync logic to make sure the module compiles with a sys_clk, it doesnt do anything
        stupid = Signal(name="stupid_only_needed_for_clk_dont_ever_use")
        self.sync += stupid.eq(stupid)

        self.builtin_outputs: list[Signal] = [stupid]
        self.builtin_inputs: list[Signal] = [stupid]

        self.__module__ = module_name

    def _save_module(
        self,
        output_dir: str = "hdl",
        module_name: str = "should_be_uniquely_named",
        ios: list[Signal] = [],
    ):
        """Save the module

        Args:
            module_name: Name of the module (without .v extension)
            ios: Set of input/output signals to include in the module interface
            output_dir: Directory to save the file
            module_name: Name of the module (without .v extension)
        """

        # Convert to Verilog
        verilog_code = verilog.convert(self, name=module_name, ios=ios)

        # Include a timescale
        verilog_code_str = f"`timescale 1ns / 1ps\n\n{verilog_code}"

        save_file(output_dir, f"{module_name}.v", verilog_code_str)

    def compile(
        self, output_dir: str = "hdl/compiled_pipelines", output_vars: list[Var] = []
    ) -> int:
        """Compile the module into a verilog file, returns the delay"""

        # Sync the outputs so everything comes out the same clock cycle, this is messy. Fuck it
        # TODO: Clean this code up if possible/feel like it
        max_delay = max([output._delay for output in output_vars] + [0])
        new_output = []
        for output in output_vars:
            while output._delay < max_delay:
                output = output.inc_delay()
            new_output.append(output)
        output_vars = new_output

        # Convert the Var objects to their underlying signals
        ios = set(
            self.builtin_inputs
            + self.builtin_outputs
            + [value._signal for value in output_vars]
        )

        self._save_module(output_dir=output_dir, module_name=self.__module__, ios=ios)

        # Calcualte the delay
        delay = 0
        if len(output_vars) > 0:
            delay = output_vars[0]._delay

        # Define the macros for this pipeline in dictionary
        macros: dict[str, str | int] = dict()
        macros[f"{self.__module__}_delay"] = delay

        # Save this into a macro file
        generate_define_file(macros, output_dir, f"{self.__module__}_defines")

        # Save the runtime python files
        generate_python_file(macros, "sim", f"{self.__module__}_runtime_constants")
