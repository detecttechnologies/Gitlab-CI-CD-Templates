#!/bin/bash

LOAD_DIR="/app/user/load"
CWD=$(pwd)
ARTIFACTS_DIR="${CWD}/artifacts"

# Create directories, copy all files to load directory
mkdir -p -v ${LOAD_DIR} ${ARTIFACTS_DIR}

# Copy all files to the loading directory
cp -R ./* ${LOAD_DIR}
echo "Copied repo files to load directory for compilation."

# Check if the variable $EXCLUDE_FILES is defined
if [ -z "${EXCLUDE_FILES}" ]; then
  echo "No files to be excluded from compilation"
else
  IFS=$'\n' read -rd '' -a exclude_files <<<"$EXCLUDE_FILES"
  for file in "${exclude_files[@]}"
  do
    file=${file#./}
    find ${LOAD_DIR} -type f -wholename "*$file*" -exec rm "{}" \;
    echo "Removed ${file} from compilation"
  done
fi

# Compile python files
echo "Starting Compilation"
echo "--------------------------------------------------------"
python3 /app/py_compiler.py build_ext -b ${LOAD_DIR}
echo "--------------------------------------------------------"
echo "Finished Compilation"

# Copy all compiled .so files to the artifacts directory
echo "Copying .so files to artifacts"
cd ${LOAD_DIR}
find . -wholename "**/*.so" -exec cp --parents \{\} ${ARTIFACTS_DIR} \;
