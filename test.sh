#!/bin/bash

# Python level tests
python3 -m test_pre_build.test_utils.test_number_conversions
python3 -m test_pre_build.test_macros.test_macros_generator
python3 -m test_pre_build.test_pipelines.test_module

# Cocotb level tests
python3 -m sim.combinational_tests
python3 -m sim.time_dependent_and_automatic_tests
python3 -m sim.signed_tests
python3 -m sim.enforce_same_bit_size