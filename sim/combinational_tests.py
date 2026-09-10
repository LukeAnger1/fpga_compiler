#!/usr/bin/env python3
# [treesource] This script does signed tests

import cocotb
import os
import sys
from pathlib import Path
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.runner import get_runner

from pre_build.pipelines.vars import Var, VarType
from pre_build.pipelines.module import MigenPipelineCompiler
from pre_build.utils.number_conversions import SignedRegValue, UnsignedRegValue

# cheap way to get the name of current file for runner:
test_file = os.path.basename(__file__).replace(".py", "")

TEST_BIT_SIZE = 5


async def generate_clock(clock_wire):
    while True:  # repeat forever
        clock_wire.value = 0
        await Timer(5, units="ns")
        clock_wire.value = 1
        await Timer(5, units="ns")


@cocotb.test()
async def test(dut):

    cocotb.start_soon(generate_clock(dut.sys_clk))
    await RisingEdge(dut.sys_clk)

    # Input the combinational logic
    dut.a.value = UnsignedRegValue(3, TEST_BIT_SIZE).get_internal()
    dut.b.value = UnsignedRegValue(2, TEST_BIT_SIZE).get_internal()

    await ReadOnly()

    assert dut.a_1.value == UnsignedRegValue(5, TEST_BIT_SIZE).get_internal(), (
        f"Not adding correctly"
    )
    assert dut.a_2.value == UnsignedRegValue(1, TEST_BIT_SIZE).get_internal()
    assert dut.a_3.value == UnsignedRegValue(6, TEST_BIT_SIZE).get_internal()
    assert dut.a_4.value == UnsignedRegValue(5, TEST_BIT_SIZE).get_internal()
    assert dut.a_5.value == UnsignedRegValue(7, TEST_BIT_SIZE).get_internal()
    assert dut.a_6.value == UnsignedRegValue(12, TEST_BIT_SIZE).get_internal()


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
        proj_path / "hdl" / "tests_dont_use" / "test_combinational_logic.v"
    ]  # grow/modify this as needed.
    hdl_toplevel = "test_combinational_logic"
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
    module = MigenPipelineCompiler("test_combinational_logic")
    a = Var(module, VarType(TEST_BIT_SIZE, False, False, False, False, True), name="a")
    b = Var(module, VarType(TEST_BIT_SIZE, False, False, False, False, True), name="b")
    c = a + b
    d = a - b
    e = a * b
    f = c | d
    g = d ^ e
    h = f + g
    module.compile(
        "hdl/tests_dont_use",
        [h],
    )


if __name__ == "__main__":
    compile_pipeline()
    runner()
