import re
import hashlib
import glob

MODULE_NAME = "rectle_core"
DIST_DIR = ".\\dist\\"
INPUT_DIR = ".\\code\\"

import_files = ""

for path in glob.iglob(f"{INPUT_DIR}/**/*.py", recursive=True):
    print(path)
    with open(path, 'r') as file:
        data = file.read()

    pattern = r"((?:#)|(?:\"\"\"\{))% (\w+)\.(\w+)\.(\w+)(.*) %((?:#)|(?:\}\"\"\"))"

    matches = re.findall(pattern, data)

    for match in matches:
        print(match)
        _prefix, _scope, _type, _name, _args, _suffix = match
        if (_scope.upper() != "RECTLE"):
            continue
        
        print(_name.lower())
        if _type.upper() == "FUNC":
            args_str = ", ".join(_args.strip().split(" "))
            print(args_str)

            function_name = hashlib.sha256(_name.lower().encode()).hexdigest()
            function_call = f"{MODULE_NAME}.rectle_{function_name}.{_name.lower()}({args_str})"
            data = data.replace(f"{_prefix}% {_scope}.{_type}.{_name}{_args} %{_suffix}", function_call)

            import_files += f"import {MODULE_NAME}.rectle_{function_name}\n"

            
        if _type.upper() == "VAR":
            variable_name = hashlib.sha256(_name.lower().encode()).hexdigest()
            variable_ref = f"{MODULE_NAME}.rectle_{variable_name}.{_name.upper()}"
            data = data.replace(f"{_prefix}% {_scope}.{_type}.{_name}{_args} %{_suffix}", variable_ref)

            import_files += f"import {MODULE_NAME}.rectle_{variable_name}\n"

    with open(path.replace(INPUT_DIR, DIST_DIR), 'w') as file:
        file.write("\n".join([import_files, data]))