#!/usr/bin/env python3
"""
# [treesource] Generate a Verilog file with define for macros
"""

from pre_build.utils.file_operations import save_file


def generate_define_file(
    defines_dict: dict[str, (str | int)],
    output_dir: str = "hdl",
    module_name: str = "defines",
):
    """
    Generate a Verilog file with `define statements

    Args:
        defines_dict: Dictionary of define name -> value
        filename: Output Verilog filename
    """

    # Simple make the lines
    lines: list[str] = []
    for name, value in defines_dict.items():
        lines.append(f"`define {name} {value}")

    # Write to file
    save_file(output_dir, module_name + ".v", "\n".join(lines))
