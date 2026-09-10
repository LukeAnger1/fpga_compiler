#!/usr/bin/env python3
"""
# [treesource] This is the module class that can be converted to verilog module amongst other things
"""

from migen import *
from migen.fhdl import verilog

from pre_build.utils.file_operations import save_file
from pre_build.pipelines.types import VarType, ModuleType, NONE, PYTHON, CALYX, MIGEN


# This is the parent class
#   When making a new backend, make a child of this class
class CustomParentModule(Module):
    type = ModuleType(NONE)
    unique_name_tracker: set[str] = set()


class MigenPipelineCompiler(CustomParentModule):
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

        # Macros dictionary
        self.macros = {}

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
    ):
        """Compile the module into a verilog file"""

        # IMPORTANT TODO: Go through the comments below and decide what to add or not
        # Sync the outputs so everything comes out the same clock cycle, this is messy. Fuck it
        # outputs = sync_outputs(outputs)

        # Convert the Var objects to their underlying signals
        ios = set(
            self.builtin_inputs
            + self.builtin_outputs
            + [value._signal for value in output_vars]
        )

        # # Add in the signals
        # ios_signals = {var._signal for var in ios}

        # # Add in the builtin signals
        # ios_signals.update(
        #     {signal for signal in self.builtin_inputs + self.builtin_outputs}
        # )

        # # Add in the signals that are passed in as arguments for more flexibility
        # ios_signals.update(input_signals)
        # ios_signals.update(output_signals)

        # # Calculate the delay from the input signals to the output signals
        # # IMPORTANT NOTE: This assumes the output delays have been synchronized
        # delay = outputs[0]._delay - inputs[0]._delay
        # self.macros[f"{self.__module__}_delay"] = delay

        # # Include the delay in a specialized macro file for the module
        # generate_define_file(self.macros, "hdl/compiled_macros", self.__module__)

        self._save_module(output_dir=output_dir, module_name=self.__module__, ios=ios)

        # Return the output variables as they have changed, useful for debugging
        # return outputs
