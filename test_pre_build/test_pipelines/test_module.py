#!/usr/bin/env python3
"""
# [treesource] This is the python file to test the code
"""

from pre_build.pipelines.module_implementation.migen import MigenPipelineCompiler
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
    a = Var(module, VarType(5, False, True, True, False, False))
    b = Var(module, VarType(5, False, True, True, False, False))
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
    a = Var(module, VarType(5, False, True, True, False, False), name="a")
    b = Var(module, VarType(5, False, True, True, False, False), name="b")
    a = a + b
    b = a + b
    a = a + b
    b = a + b
    module.compile(
        "hdl/tests_dont_use",
        [a, b],
    )


# TODO: Should add in logic to try to simplify logic from known constant values
#   EX: They are not time dependent
def test_operations_migen_pipeline_constant():
    module = MigenPipelineCompiler("test_math_operations_constant_pipeline")
    a = Var(
        module,
        VarType(5, False, False, False, False, False),
        constant_value=1,
        name="a",
    )
    b = Var(module, VarType(5, False, False, False, False, False), name="b")
    a = a + b
    b = a + b
    a = a + b
    b = a + b
    module.compile(
        "hdl/tests_dont_use",
        [a, b],
    )


def test_operations_migen_pipeline_time_dependent():
    module = MigenPipelineCompiler("test_math_operations_time_dependent")
    a = Var(
        module,
        VarType(5, False, True, False, False, False),
        name="a",
    )
    b = Var(module, VarType(5, False, False, False, False, False), name="b")
    c = Var(
        module,
        VarType(5, False, True, False, False, False),
        name="c",
    )
    a = a + c
    a = a + b
    b = a + b
    a = a + b
    b = a + b
    module.compile(
        "hdl/tests_dont_use",
        [a, b],
    )


def test_failure_on_different_bit_size():
    module = MigenPipelineCompiler("test_math_operations_time_dependent")
    a = Var(
        module,
        VarType(10, False, True, False, False, True),
        name="a",
    )
    b = Var(module, VarType(5, False, False, False, False, True), name="b")
    c = Var(
        module,
        VarType(7, False, True, False, False, False),
        name="c",
    )

    failed_to_throw = True
    try:
        a + c
    except:
        failed_to_throw = False
    if failed_to_throw:
        raise ValueError(
            f"failed to throw error when one wants enforced bit sizes and not other"
        )

    failed_to_throw = True
    try:
        a + b
    except:
        failed_to_throw = False
    if failed_to_throw:
        raise ValueError(
            f"expected a failure as it is type enforced and different sizes"
        )


# IMPORTANT TODO: Check pipelining for multiple layers

if __name__ == "__main__":
    test_simple_migen_compilation()
    test_constant_value_migen_compilation()
    test_operations_migen_compilation()
    test_operations_migen()
    test_operations_migen_pipeline()
    test_operations_migen_pipeline_constant()
    test_operations_migen_pipeline_time_dependent()
    test_failure_on_different_bit_size()
    print(f"tests passed {__file__}")
