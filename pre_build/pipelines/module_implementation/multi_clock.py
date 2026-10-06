#!/usr/bin/env python3
"""
# [treesource] This is a class that generates a module with multiple clock

There is a single fast clock (sys_clk). A register width of N runs N copies of its module, each N times slower.
    The slow clocks come from a ring of N registers with a single 1 that shifts every fast cycle,
    copy k only updates its registers on the fast cycles that ring bit k is active.
    Delays are tracked in fast clock cycles, at any fast cycle the active copy is the one that holds the current values.
"""

from migen import *
from migen.fhdl.tools import list_signals, list_targets
from migen.fhdl.visit import NodeTransformer

from pre_build.pipelines.types import (
    VarType,
    ModuleType,
    MIGEN,
    MULTI,
)
from pre_build.pipelines.module_implementation.parent import CustomParentModule
from pre_build.pipelines.module_implementation.migen import MigenPipelineCompiler


# Swaps the signals in statements, used to make the copies of a module
class _SignalReplacer(NodeTransformer):
    def __init__(self, mapping: dict[Signal, Signal]) -> None:
        self.mapping = mapping

    def visit_Signal(self, node):
        return self.mapping.get(node, node)


class MultiClockPipelineCompiler(CustomParentModule):
    type = ModuleType(MULTI)

    def __init__(self, module_name: str, sub_module_type: str = MIGEN) -> None:
        # A new module of the choosen type is built whenever a new clock is added in
        self.sub_module_type = ModuleType(sub_module_type)

        # This dictionary maps the register widths with the corresponding modules
        self.register_width_mapping: dict[int, CustomParentModule] = dict()

        # The (source, destination) signals that cross between clocks
        self.crossings: list[tuple[Signal, Signal]] = []

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

    def stage_delay(self, varType: VarType) -> int:
        # A register in a clock N times slower takes N fast cycles
        return varType._register_width

    def connect_register_width(self, source: "Var", destination: "Var"):
        # The wiring is done when building the top module
        self.crossings.append((source._signal, destination._signal))

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
    ) -> int:
        """Compile all the clocks into a single top module, returns the delay in fast clock cycles"""

        # Sync the outputs so everything comes out the same fast clock cycle
        max_delay = max([output._delay for output in output_vars] + [0])
        new_output = []
        for output in output_vars:
            while output._delay < max_delay:
                output = output.inc_delay()
            new_output.append(output)
        output_vars = new_output

        output_signals = {output._signal for output in output_vars}
        crossing_sources = {source for source, _ in self.crossings}
        crossing_destinations = {destination for _, destination in self.crossings}

        # The top module holds the fast clock, the rings, and all the copies
        top = MigenPipelineCompiler(self.__module__)
        primary_inputs: list[Signal] = []

        for register_width, module in sorted(self.register_width_mapping.items()):
            fragment = module.get_fragment()
            assert set(fragment.sync.keys()) <= {"sys"}, (
                f"Only the sys clock is supported in the sub modules"
            )
            signals = list_signals(fragment) | set(module.builtin_inputs)
            driven = list_targets(fragment)

            # Anything not driven inside the clock module has to come from outside
            for signal in module.builtin_inputs:
                if signal not in driven and signal not in crossing_destinations:
                    primary_inputs.append(signal)

            # The fast clock is the module itself
            if register_width == 1:
                top.comb += _SignalReplacer({}).visit(fragment.comb)
                top.sync += _SignalReplacer({}).visit(fragment.sync.get("sys", []))
                continue

            # Ring of N registers with a single active bit, shifts by one every fast cycle
            ring = Signal(register_width, reset=1, name=f"ring_{register_width}")
            top.sync += ring.eq(
                Cat(ring[register_width - 1], ring[: register_width - 1])
            )

            # The original signals are used as the view of the copies from the outside
            #   Inputs are sent to every copy, the outputs are taken from the active copy
            muxed_signals = [
                signal
                for signal in signals
                if signal in driven
                and (signal in output_signals or signal in crossing_sources)
            ]
            for signal in muxed_signals:
                top.comb += signal.eq(0)

            for copy in range(register_width):
                mapping = {
                    signal: Signal.like(
                        signal, name_override=f"{self._signal_name(signal)}_copy{copy}"
                    )
                    for signal in signals
                }
                replacer = _SignalReplacer(mapping)

                top.comb += replacer.visit(fragment.comb)
                # The copy only updates on its slow clock
                copy_sync = replacer.visit(fragment.sync.get("sys", []))
                if len(copy_sync) > 0:
                    top.sync += If(ring[copy], *copy_sync)

                for signal in signals:
                    if signal not in driven:
                        top.comb += mapping[signal].eq(signal)
                for signal in muxed_signals:
                    top.comb += If(ring[copy], signal.eq(mapping[signal]))

        # Wire the clocks together, both sides are the outside view so it is a direct connection
        for source, destination in self.crossings:
            top.comb += destination.eq(source)

        ios = set(top.builtin_outputs + primary_inputs + list(output_signals))
        top._save_module(output_dir=output_dir, module_name=self.__module__, ios=ios)
        top._save_macros(output_dir, max_delay)

        return max_delay

    @staticmethod
    def _signal_name(signal: Signal) -> str:
        if signal.name_override is not None:
            return signal.name_override
        return signal.backtrace[-1][0] or "signal"
