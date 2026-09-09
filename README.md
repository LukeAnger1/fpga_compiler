This is a repo to streamline FPGA development for code.

The goal of this repo is to generate verilog code.

Features to be included are

Backends
1. migen for verilog compilation without optimizations
2. calyx for verilog compilation with optimizations
3. simulate in python directly without compilation

Features
I want to include clock modifications, this would allow double clocking certain sections of pipelines to run faster
These would only allow modifications with 2^n for simplicity with the clock

Format
Make sure to format everything with ruff format

Test
Run test.sh to run the tests