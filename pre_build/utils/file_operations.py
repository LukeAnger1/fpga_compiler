def save_file(
    output_dir: str = "folder_to_save",
    file_name: str = "should_be_uniquely_named",
    contents: str = "",
):
    """Save the module

    Args:
       output_dir: Directory to save the file
       file_name: Name of the file (with the extension)
       contents: Contents to write to the file
    """

    # Write to file
    filepath = f"{output_dir}/{file_name}"
    with open(filepath, "w") as f:
        f.write(contents)
