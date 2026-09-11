#!/usr/bin/env python3
"""
# [treesource] Generate a Python file with constants that can be used
"""

from pre_build.utils.file_operations import save_file


def generate_python_file(
    defines_dict: dict[str, (str | int)],
    output_dir: str = "sim",
    module_name: str = "runtime_constants",
):
    """
    Generate a Python file with `define statements

    Args:
        defines_dict: Dictionary of define name -> value
        filename: Output python filename
    """

    # Simple make the lines
    lines: list[str] = []
    for name, value in defines_dict.items():
        lines.append(f"{name} = {value}")

    # Write to file
    save_file(output_dir, module_name + ".py", "\n".join(lines))
