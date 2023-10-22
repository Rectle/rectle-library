import py_compile
import os
import shutil
import re
import hashlib
import glob
import sys

MODULE_NAME = "rectle_core"
CORE_DIR = "./src/rectle_lib/src/core/"

try:
   DIST_DIR = str(sys.argv[1]) + f"/{MODULE_NAME}/"
except:
   DIST_DIR = f"./dist/{MODULE_NAME}/"
# Setup

if os.path.exists(DIST_DIR):
   shutil.rmtree(DIST_DIR)

os.makedirs(DIST_DIR)

# Build

for path in glob.iglob(f"{CORE_DIR}/**/*.py", recursive=True):
   with open(path, 'r') as file:
      original_file = file.read()

   pattern = r".*(?:\\|\/)([^\.]+\.py)"

   try: 
      file_name = re.findall(pattern, path)[0].split('.')[0]

      hash_name = hashlib.sha256(file_name.lower().encode())
      file_name = hash_name.hexdigest()
      
      py_compile.compile(path, cfile=f"{DIST_DIR}rectle_{file_name}.pyc", doraise=True)
   except:
      pass
