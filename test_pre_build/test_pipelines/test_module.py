#!/usr/bin/env python3
"""
# [treesource] This is the python file to test the code
"""

from pre_build.pipelines.module import MigenPipelineCompiler
from pre_build.pipelines.vars import Var, VarType


def test_simple_migen_compilation():
    module = MigenPipelineCompiler("test_compilation")
    module.compile("hdl/tests_dont_use")


def test_constant_value_migen_compilation():
    module = MigenPipelineCompiler("test_constant_value")
    module.compile("hdl/tests_dont_use")


def test_operations_migen_compilation():
    pass  # TODO: Finsih implementing this
    # module = MigenPipelineCompiler("test_math_operations")
    # a = Var(module, VarType(5, False, True, True, False))
    # b = Var(module, VarType(5, False, True, True, False))
    # # a = abs(a)
    # c = a + b
    # d = a - b
    # e = c * d
    # f = e > a
    # g = a < f
    # h = a <= g
    # i = a >= b
    # module.compile("hdl/tests_dont_use", [h, i])

    # module = MigenPipelineCompiler("test_math_operations_2")
    # a = Var(module, VarType(5, True, True, True, False))
    # a = abs(a)
    # module.compile("hdl/tests_dont_use")


def test_operations_migen():
    module = MigenPipelineCompiler("test_math_operations_execution")
    a = Var(module, VarType(5, False, True, True, False))
    b = Var(module, VarType(5, False, True, True, False))
    module.compile(
        "hdl/tests_dont_use",
        [
            a + b,
            a - b,
            a * b,
            a > b,
            a < b,
            a >= b,
            a <= b,
            ~a,
            a ^ b,
            a == b,
            a != b,
            a & b,
            a | b,
        ],
    )


def test_operations_migen_pipeline():
    module = MigenPipelineCompiler("test_math_operations_pipeline")
    a = Var(module, VarType(5, False, True, True, False), name="a")
    b = Var(module, VarType(5, False, True, True, False), name="b")
    a = a + b
    b = a + b
    a = a + b
    b = a + b
    module.compile(
        "hdl/tests_dont_use",
        [a, b],
    )


# IMPORTANT TODO: Add in logic to check the constant value in pipeline

if __name__ == "__main__":
    test_simple_migen_compilation()
    test_constant_value_migen_compilation()
    test_operations_migen_compilation()
    test_operations_migen()
    test_operations_migen_pipeline()
    print(f"tests passed {__file__}")
