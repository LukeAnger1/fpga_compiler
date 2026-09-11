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

I want to add in a static message passing operation and dynamic one. This would require setting up dynamic then having a pass to see if the message would be gauranteed to be sent before the read in the pipeline to promote to static

Add logic to track all defines to make sure there are no conflicting ones

Format
Make sure to format everything with ruff format

Test
Run test.sh to run the tests

I want to add in clock gating according to the below to ensure hardware has less area and easier to implement
https://anysilicon.com/the-ultimate-guide-to-clock-gating/?hl=en-US

Add in backends
CIRCT https://circt.llvm.org/docs/PyCDE/
CALYX
