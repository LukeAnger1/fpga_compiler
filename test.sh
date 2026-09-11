#!/bin/bash

# Exit on failure
set -e

# Python level tests
python3 -m test_pre_build.test_utils.test_number_conversions
python3 -m test_pre_build.test_macros.test_macros_generator
python3 -m test_pre_build.test_pipelines.test_module

# Cocotb level tests
#   This tests dont properly fail
#   Saving them in another file and failing for certain keywords
python3 -m sim.combinational_tests > tmp
if grep -q "test failed" tmp; then
    cat tmp
    exit
else
    echo "passed combinational tests"
fi

python3 -m sim.time_dependent_and_automatic_tests > tmp
if grep -q "test failed" tmp; then
    cat tmp
    exit
else
    echo "passed time dependent tests"
fi

python3 -m sim.signed_tests > tmp
if grep -q "test failed" tmp; then
    cat tmp
    exit
else
    echo "passed signed tests"
fi

python3 -m sim.enforce_same_bit_size > tmp
if grep -q "test failed" tmp; then
    cat tmp
    exit
else
    echo "passed bit size tests"
fi

python3 -m sim.pipeline_timing_tests > tmp
if grep -q "test failed" tmp; then
    cat tmp
    exit
else
    echo "passed timing tests"
fi