#!/usr/bin/env python3
# [treesource] This script tests all the equality operations with different sizes too

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

SMALL_BIT_SIZE = 5
BIG_BIT_SIZE = 10


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

    # Positive compared to positive tests
    NUM_1 = 1
    NUM_2 = 2
    NUM_3 = 3

    dut.signed_small_bit_size.value = SignedRegValue(
        NUM_1, SMALL_BIT_SIZE
    ).get_internal()
    dut.signed_big_bit_size.value = SignedRegValue(NUM_2, BIG_BIT_SIZE).get_internal()
    dut.signed_small_bit_size2.value = SignedRegValue(
        NUM_3, SMALL_BIT_SIZE
    ).get_internal()
    dut.unsigned_small_bit_size.value = SignedRegValue(
        NUM_1, SMALL_BIT_SIZE
    ).get_internal()
    dut.unsigned_big_bit_size.value = SignedRegValue(NUM_2, BIG_BIT_SIZE).get_internal()
    dut.unsigned_small_bit_size2.value = SignedRegValue(
        NUM_3, SMALL_BIT_SIZE
    ).get_internal()

    await RisingEdge(dut.sys_clk)
    await ReadOnly()

    assert (dut.signed_small_bit_size_1.value) == (NUM_1 < NUM_3)
    assert (dut.signed_small_bit_size_2.value) == (NUM_1 > NUM_3)
    assert (dut.signed_small_bit_size_3.value) == (NUM_1 == NUM_3)

    assert (dut.signed_small_bit_size_5.value) == (NUM_1 < NUM_2)
    assert (dut.signed_small_bit_size_7.value) == (NUM_1 > NUM_2)
    assert (dut.signed_small_bit_size_9.value) == (NUM_1 == NUM_2)

    # Positive comparted to negative tests

    # Negative compared to negative tests

    # Positive compared to 0, Negative compared to 0


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
        proj_path / "hdl" / "tests_dont_use" / "test_equality_operations.v"
    ]  # grow/modify this as needed.
    hdl_toplevel = "test_equality_operations"
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


def compile_pipeline_equality_operations():
    module = MigenPipelineCompiler("test_equality_operations")
    signed_small_bit_size = Var(
        module,
        VarType(SMALL_BIT_SIZE, True, False, False, False, False),
        name="signed_small_bit_size",
    )
    signed_big_bit_size = Var(
        module,
        VarType(BIG_BIT_SIZE, True, False, False, False, False),
        name="signed_big_bit_size",
    )
    signed_small_bit_size2 = Var(
        module,
        VarType(SMALL_BIT_SIZE, True, False, False, False, False),
        name="signed_small_bit_size2",
    )
    unsigned_small_bit_size = Var(
        module,
        VarType(SMALL_BIT_SIZE, True, False, False, False, False),
        name="unsigned_small_bit_size",
    )
    unsigned_big_bit_size = Var(
        module,
        VarType(BIG_BIT_SIZE, True, False, False, False, False),
        name="unsigned_big_bit_size",
    )
    unsigned_small_bit_size2 = Var(
        module,
        VarType(SMALL_BIT_SIZE, True, False, False, False, False),
        name="unsigned_small_bit_size2",
    )

    signed_small_bit_size < signed_small_bit_size2
    signed_small_bit_size > signed_small_bit_size2
    signed_small_bit_size == signed_small_bit_size2

    signed_small_bit_size < signed_big_bit_size
    signed_small_bit_size > signed_big_bit_size
    signed_small_bit_size == signed_big_bit_size

    signed_small_bit_size < unsigned_small_bit_size
    signed_small_bit_size > unsigned_small_bit_size
    signed_small_bit_size == unsigned_small_bit_size

    unsigned_small_bit_size < unsigned_small_bit_size
    unsigned_small_bit_size > unsigned_small_bit_size
    unsigned_small_bit_size == unsigned_small_bit_size

    unsigned_small_bit_size < unsigned_big_bit_size
    unsigned_small_bit_size > unsigned_big_bit_size
    unsigned_small_bit_size == unsigned_big_bit_size

    module.compile(
        "hdl/tests_dont_use",
        [],
    )


if __name__ == "__main__":
    compile_pipeline_equality_operations()
    runner()
