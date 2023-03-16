#!/bin/bash

# Create directory for loading files
mkdir -p /app/user/load

# Copy all files to the loading directory
cp -R ./* /app/user/load

# Navigate to the loading directory
cd /app/user/load
rm -rfv scripts # So that .py files inside don't get compiled

# Check if the variable $EXCLUDE_FILES is defined
if [ -z "$EXCLUDE_FILES" ]; then
  echo "EXCLUDE_FILES is not defined"
else
  # Exclude any python file from cythonization
  for file in $EXCLUDE_FILES
  do
    find . -wholename "$file" -exec rm -v "{}" \;
  done
fi

# Navigate back to the previous directory
cd -

# Navigate to the root directory
cd /app

# Compile python files using py_compiler.py
python3 py_compiler.py build_ext -b /app/user/load

# Navigate back to the previous directory
cd -

# Create directory for compiled files
cwd=$(pwd)
mkdir artifacts

# Navigate to the loading directory
cd /app/user/load/

# Copy all compiled .so files to the artifacts directory
find . -wholename "**/*.so" -exec cp -v --parents \{\} $cwd/artifacts \;
