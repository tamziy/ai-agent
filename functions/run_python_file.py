import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        is_valid_target_file_path = os.path.commonpath((working_dir_abs_path, target_file_path)) == working_dir_abs_path
        if not is_valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        command_proccesser = subprocess.run(command, capture_output=True, text=True, timeout=60)

        result_str = ""
        if command_proccesser.returncode != 0:
            result_str += "Process exited with code X"
            
        if command_proccesser.stdout is None and command_proccesser.stderr is None:
            result_str += "No output produced"
        else:
            if command_proccesser.stdout:
                result_str += f"STDOUT: {command_proccesser.stdout}"
            if command_proccesser.stderr:
                result_str += f"STDERR: {command_proccesser.stderr}"
        
        return result_str
    except Exception as e:
        return f"Error: executing Python file: {e}"