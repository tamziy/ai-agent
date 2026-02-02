import os
from config import CHARACTER_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
        try:
            working_dir_abs_path = os.path.abspath(working_directory)
            target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

            is_valid_target_file_path = os.path.commonpath((working_dir_abs_path, target_file_path)) == working_dir_abs_path
            if not is_valid_target_file_path:
                return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory' 
                
            if not os.path.isfile(target_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
            
            with open(target_file_path, mode='r') as f:
                contents = f.read(CHARACTER_LIMIT)
                if f.read(1):
                    contents += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            
            return contents
        except Exception as e:
            return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file up to 10000 characters before truncating",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the desired file to be read, relative to the working directory"
            ),
        },
    ),
)