#!/usr/bin/env python3
# [treesource] This script tests the pipelining to make sure all signals on the output are synced and meet the proper timing

# This should include tests to make sure all signals are at the end of the pipeline and proper

import cocotb
import os
import sys
from pathlib import Path
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.runner import get_runner

from pre_build.pipelines.vars import Var, VarType
from pre_build.pipelines.module_implementation.migen import MigenPipelineCompiler
from pre_build.utils.number_conversions import SignedRegValue, UnsignedRegValue

# cheap way to get the name of current file for runner:
test_file = os.path.basename(__file__).replace(".py", "")


async def generate_clock(clock_wire):
    while True:  # repeat forever
        clock_wire.value = 0
        await Timer(5, units="ns")
        clock_wire.value = 1
        await Timer(5, units="ns")


@cocotb.test()
async def test(dut):
    from sim.test_timing_runtime_constants import test_timing_delay

    cocotb.start_soon(generate_clock(dut.sys_clk))
    await RisingEdge(dut.sys_clk)

    BIT_SIZE = 10
    assert test_timing_delay is not None, f"the pipeline delay is {PIPELINE_DELAY}"

    # Input the combinational logic
    dut.a.value = SignedRegValue(3, BIT_SIZE).get_internal()
    dut.b.value = SignedRegValue(4, BIT_SIZE).get_internal()

    # Change the inputs on the next cycle to make sure the timing works just write
    await RisingEdge(dut.sys_clk)
    dut.a.value = 0
    dut.b.value = 0

    # Requires time to go through the pipeline
    for _ in range(test_timing_delay - 1):
        await RisingEdge(dut.sys_clk)

    await ReadOnly()

    assert dut.b_2.value == SignedRegValue(11, BIT_SIZE).get_internal()
    assert dut.a_2.value == SignedRegValue(7, BIT_SIZE).get_internal()
    assert dut.b_2.value == SignedRegValue(11, BIT_SIZE).get_internal()

    # Make sure on the next cycle that the outputs are different
    await RisingEdge(dut.sys_clk)
    await ReadOnly()
    assert dut.b_2.value != SignedRegValue(11, BIT_SIZE).get_internal()
    assert dut.a_2.value != SignedRegValue(7, BIT_SIZE).get_internal()
    assert dut.b_2.value != SignedRegValue(11, BIT_SIZE).get_internal()


"""the code below should largely remain unchanged in structure, though the specific files and things
specified should get updated for different simulations.
"""


def runner():
    """Simulate the generate code modules using the Python runner."""
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(proj_path / "sim" / "model"))
    sources = [
        proj_path / "hdl" / "tests_dont_use" / "test_timing.v",
    ]  # grow/modify this as needed.
    hdl_toplevel = "test_timing"
    build_test_args = ["-Wall"]  # ,"COCOTB_RESOLVE_X=ZEROS"]
    parameters = {}
    sys.path.append(str(proj_path / "sim"))
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=hdl_toplevel,
        always=True,
        build_args=build_test_args,
        parameters=parameters,
        timescale=("1ns", "1ps"),
        waves=True,
    )
    run_test_args = []
    runner.test(
        hdl_toplevel=hdl_toplevel,
        test_module=test_file,
        test_args=run_test_args,
        waves=True,
    )


def compile_pipeline():
    module = MigenPipelineCompiler("test_timing")
    a = Var(module, VarType(5, True, True, True, False, False), name="a")
    b = Var(module, VarType(5, True, True, True, False, False), name="b")
    c = a + b
    d = b + c
    module.compile(
        "hdl/tests_dont_use",
        [b, c, d],
    )


if __name__ == "__main__":
    compile_pipeline()
    runner()
