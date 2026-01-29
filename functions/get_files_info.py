import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(working_dir_abs_path, directory))

        is_valid_target_dir = os.path.commonpath((working_dir_abs_path, target_dir_path)) == working_dir_abs_path
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
            
        if not os.path.isdir(target_dir_path):
            return f'Error: "{directory}" is not a directory'
        
        dir_contents = []
        target_dir_items = os.listdir(target_dir_path)
        for item in target_dir_items:
            item_path = os.path.normpath(os.path.join(target_dir_path, item))
            dir_contents.append(f"  - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

        return "\n".join(dir_contents)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)