#!/bin/bash
set -euo pipefail

NPROC=$(nproc)
LOAD_DIR="/app/user/load"
CWD=$(pwd)
ARTIFACTS_DIR="${CWD}/artifacts"

echo "Detected ${NPROC} CPU cores — will parallelize where possible."

# Create directories, copy all files to load directory
mkdir -p ${LOAD_DIR} ${ARTIFACTS_DIR}

# Copy all files to the loading directory
cp -R ./* ${LOAD_DIR}
echo "Copied repo files to load directory for compilation."

# Check if the variable $EXCLUDE_FILES is defined
if [ -z "${EXCLUDE_FILES:-}" ]; then
  echo "No files to be excluded from compilation"
else
  IFS=$'\n' read -rd '' -a exclude_files <<<"$EXCLUDE_FILES" || true
  for file in "${exclude_files[@]}"
  do
    file=${file#./}
    find ${LOAD_DIR} -type f -wholename "*$file*" -delete -print | sed 's/^/Removed: /'
  done
fi

# Compile python files using all available cores
echo "Starting Compilation (parallel: ${NPROC} jobs)"
echo "--------------------------------------------------------"
python3 /app/py_compiler.py build_ext -b ${LOAD_DIR} -j ${NPROC} || exit 1
echo "--------------------------------------------------------"
echo "Finished Compilation"

# Copy all compiled .so files to the artifacts directory in parallel
echo "Copying .so files to artifacts"
cd ${LOAD_DIR}
find . -name "*.so" -print0 | xargs -0 -P ${NPROC} -I{} bash -c 'mkdir -p "'"${ARTIFACTS_DIR}"'/$(dirname "{}")" && cp "{}" "'"${ARTIFACTS_DIR}"'/{}"'
