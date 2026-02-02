import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        is_valid_target_file_path = os.path.commonpath((working_dir_abs_path, target_file_path)) == working_dir_abs_path
        if not is_valid_target_file_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory' 
            
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the desired file. Overwrites the content of an existing file, or creates a new file if it doesn't exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the desired file to be written, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the desired file"
            ),
        },
    ),
)