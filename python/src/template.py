import re
import hashlib
import py_compile
import os

MODULE_NAME = "rectle_module"

# Setup
with open('./src/rectle.py', 'r') as config_file:
   config_data = config_file.read()

# Replace functions names
pattern = r"def\s+(\w+)\s*\("
matches = re.findall(pattern, config_data)

for match in matches:
    hash_object = hashlib.sha256(match.encode())
    hash_hex = f'_f{hash_object.hexdigest()}'

    config_data = re.sub(rf"\b{match}\b", hash_hex, config_data)

with open(f'{MODULE_NAME}.tmp', "w") as file:
    file.write(config_data)

py_compile.compile(f'{MODULE_NAME}.tmp', cfile=f"{MODULE_NAME}.pyc", doraise=True)

os.remove(f'{MODULE_NAME}.tmp')

# Replace variables names
pattern = r"([A-Z]+)_([A-Z_]+)\s?="
matches = re.findall(pattern, config_data)
print("matches: ", matches)
for match in matches:
    _scope, _name = match
    if _scope.upper() != "RECTLE":
        continue

    hash_object = hashlib.sha256(_name.encode())
    hash_hex = f'_v{hash_object.hexdigest()}'
    
    config_data = re.sub(rf"\b{'_'.join(match)}\b", hash_hex, config_data)

# Data

with open('./src/main.py', 'r') as data_file:
   data = data_file.read()

pattern = r"((?:#)|(?:\"\"\"\{))% (\w+)\.(\w+)\.(\w+)(.*) %((?:#)|(?:\}\"\"\"))"

matches = re.findall(pattern, data)

for match in matches:
    print(match)
    _prefix, _scope, _type, _name, _args, _suffix = match
    if (_scope.upper() != "RECTLE"):
        continue

    if _type.upper() == "FUNC":
        args_str = ", ".join(_args.strip().split(" "))
        print(args_str)

        function_name = hashlib.sha256(_name.encode()).hexdigest()
        function_call = f"{MODULE_NAME}._f{function_name}({args_str})"
        data = data.replace(f"{_prefix}% {_scope}.{_type}.{_name}{_args} %{_suffix}", function_call)

        
    if _type.upper() == "VAR":
        variable_name = f"{MODULE_NAME}._v{hashlib.sha256(_name.encode()).hexdigest()}"
        data = data.replace(f"{_prefix}% {_scope}.{_type}.{_name}{_args} %{_suffix}", variable_name)

print(data)

load_module_script = f'''
import {MODULE_NAME}
'''

separator = f'\n{"#" * 80}\n'

with open('output.py', 'w') as output_file:
    output_file.write(load_module_script + separator + data)