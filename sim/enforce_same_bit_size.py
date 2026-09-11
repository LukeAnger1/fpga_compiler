#!/usr/bin/env python3
# [treesource] This script tests the bit sizes for signed and unsigned math

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
TEST_BIT_SIZE_2 = 10
MAX_BIT_SIZE = max(TEST_BIT_SIZE, TEST_BIT_SIZE_2)


async def generate_clock(clock_wire):
    while True:  # repeat forever
        clock_wire.value = 0
        await Timer(5, units="ns")
        clock_wire.value = 1
        await Timer(5, units="ns")


NUM_1 = 3
NUM_2 = 0
NUM_3 = -2
NUM_4 = -3


@cocotb.test()
async def test(dut):

    cocotb.start_soon(generate_clock(dut.sys_clk))
    await RisingEdge(dut.sys_clk)

    # Input the combinational logic
    dut.a.value = SignedRegValue(NUM_1, TEST_BIT_SIZE).get_internal()
    dut.b.value = SignedRegValue(NUM_2, TEST_BIT_SIZE_2).get_internal()
    dut.c.value = SignedRegValue(NUM_3, TEST_BIT_SIZE).get_internal()
    dut.d.value = SignedRegValue(NUM_4, TEST_BIT_SIZE_2).get_internal()

    # Requires time to go through the pipeline
    #   Everything is time dependent so should just have to wait awhile
    for _ in range(10):
        await RisingEdge(dut.sys_clk)

    await ReadOnly()

    assert (
        dut.a_2.value == SignedRegValue(NUM_1 + NUM_2, MAX_BIT_SIZE).get_internal()
    ), f"Not adding correctly"
    assert dut.a_4.value == SignedRegValue(NUM_1 - NUM_2, MAX_BIT_SIZE).get_internal()
    assert dut.a_6.value == SignedRegValue(NUM_1 * NUM_2, MAX_BIT_SIZE).get_internal()

    assert (
        dut.a_7.value == SignedRegValue(NUM_1 + NUM_3, TEST_BIT_SIZE).get_internal()
    ), f"Not adding correctly"
    assert dut.a_8.value == SignedRegValue(NUM_1 - NUM_3, TEST_BIT_SIZE).get_internal()
    assert dut.a_9.value == SignedRegValue(NUM_1 * NUM_3, TEST_BIT_SIZE).get_internal()

    assert (
        dut.b_1.value == SignedRegValue(NUM_2 + NUM_3, MAX_BIT_SIZE).get_internal()
    ), f"Not adding correctly"
    assert dut.b_2.value == SignedRegValue(NUM_2 - NUM_3, MAX_BIT_SIZE).get_internal()
    assert dut.b_3.value == SignedRegValue(NUM_2 * NUM_3, MAX_BIT_SIZE).get_internal()

    assert (
        dut.c_5.value == SignedRegValue(NUM_3 + NUM_4, MAX_BIT_SIZE).get_internal()
    ), f"Not adding correctly"
    assert dut.c_7.value == SignedRegValue(NUM_3 - NUM_4, MAX_BIT_SIZE).get_internal()
    assert dut.c_9.value == SignedRegValue(NUM_3 * NUM_4, MAX_BIT_SIZE).get_internal()

    assert (
        dut.a_11.value == SignedRegValue(NUM_1 + NUM_4, MAX_BIT_SIZE).get_internal()
    ), f"Not adding correctly"
    assert dut.a_13.value == SignedRegValue(NUM_1 - NUM_4, MAX_BIT_SIZE).get_internal()
    assert dut.a_15.value == SignedRegValue(NUM_1 * NUM_4, MAX_BIT_SIZE).get_internal()


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
        proj_path / "hdl" / "tests_dont_use" / "test_diff_bit_size.v"
    ]  # grow/modify this as needed.
    hdl_toplevel = "test_diff_bit_size"
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


def compile_pipeline_diff_bit_size_operations():
    module = MigenPipelineCompiler("test_diff_bit_size")
    a = Var(module, VarType(TEST_BIT_SIZE, True, True, True, False, True), name="a")
    b = Var(module, VarType(TEST_BIT_SIZE_2, True, True, True, False, True), name="b")
    c = Var(module, VarType(TEST_BIT_SIZE, True, True, True, False, True), name="c")
    d = Var(module, VarType(TEST_BIT_SIZE_2, True, True, True, False, True), name="d")
    e = a + b
    e = a - b
    e = a * b
    e = a + c
    e = a - c
    e = a * c
    e = b + c
    e = b - c
    e = b * c
    e = c + d
    e = c - d
    e = c * d
    e = a + d
    e = a - d
    e = a * d
    module.compile(
        "hdl/tests_dont_use",
        [e],
    )


if __name__ == "__main__":
    compile_pipeline_diff_bit_size_operations()
    runner()
