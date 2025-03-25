#!/bin/bash

set -x

# Copy files from artifacts to their original destination and remove artifacts folder
cwd=$(pwd)
cp -R artifacts/. "$cwd/"
rm -rf artifacts

# Run any necessary script/patch if available in RUN_SCRIPTS variable
if [ -z "$RUN_SCRIPTS" ]; then
    echo "RUN_SCRIPTS is not defined"
else
    for script in ${RUN_SCRIPTS}; do
        echo "Executing ${script}"
        bash "$script"
    done
fi

# Clone destination repo to make it available as local inside pipeline
git clone "https://oauth2:$BOT_ACCESS_TOKEN@gitlab.com/${BUILD_OUTPUT_REPO}" /root/dest

# Remove branches from remote if the variable is assigned "true"
cd /root/dest || exit
echo "Removing branches from destination repo for pushing the latest version"
git branch -r | awk -F/ '/\/linux/{print $2}' | xargs -n1 -P4 -I{} git push origin :{}
cd -

# Setup a branch for every unique deployment footprint, push to each of them
branch_names=$(find . -wholename "**/*.so" | awk -F '-' '{print $(NF-1)"-"$(NF-2)"-py"$(NF-3)}' | sort -u)
echo "Branches to be pushed: ${branch_names}"

process_branch() {
    local branch=$1
    local temp_dir=$(mktemp -d)
    local file_name_pattern=$(echo "$branch" | awk -F '-' '{print $3"-"$2"-"$1}')
    file_name_pattern=${file_name_pattern:2}

    # Clone the destination repo into a temporary directory
    cp -R /root/dest/. "$temp_dir"
    cd "$temp_dir" || exit
    git checkout --quiet main
    git checkout --quiet "$branch" 2>/dev/null || git checkout -b "$branch"

    cd - || exit
    echo "Copying files for branch $branch"

    # Copy files defined in COPY_FILES
    for file in ${COPY_FILES}; do
        if [[ "$file" == *"-->"* ]]; then
            split=(${file//-->/ })
            cp -R -v "${split[0]}" "${temp_dir}/${split[1]}"
        else
            find . -type f -wholename "*$file*" ! -wholename "./*.git*" -exec cp --parents {} "$temp_dir/" \;
        fi
    done

    # Remove any pre-existing `.so` files that do not match the branch
    find "$temp_dir" -type f -name "*cpython*.so" -exec rm -v "{}" \;

    # Copy the new `.so` files that match the current branch
    find . -type f -name "*${file_name_pattern}*.so" ! -name "./iva.**.so" -exec cp --parents {} "$temp_dir/" \;

    # Copy main.py and iva.py, if they exist
    echo "Copying main.py and iva.py"
    cp -v ./main.py "$temp_dir/" || echo "main.py not found, skipping"
    cp -v ./iva.py "$temp_dir/" || echo "iva.py not found, skipping"

    # Ensure __init__.py files are copied
    echo "Copying __init__.py files"
    find . -wholename "**/__init__.py" -exec cp --parents {} "$temp_dir/" \;

    # Rename filenames to original names
    cd "$temp_dir" || exit
    for f in $(find . -type f -name "*.so"); do
        mv "$f" "${f/.cpython-${file_name_pattern}-gnu./.}" || mv "$f" "${f/.cpython-${file_name_pattern}-gnueabihf./.}"
    done

    # Get the timestamp of the last commit from the source repo
    timestamp=$(git log -1 --format=%cd --date=local)

    # Stage changes, commit, and push
    git add -A
    git commit -m "Commit in source pipeline at timestamp:$timestamp" --allow-empty
    git reset $(git commit-tree HEAD^{tree} -m "Commit in source pipeline at timestamp:$timestamp")
    git push --quiet origin HEAD:"$branch" -f

    cd - || exit
    rm -rf "$temp_dir"
}

export -f process_branch
export COPY_FILES
export BOT_ACCESS_TOKEN
export BUILD_OUTPUT_REPO

echo "$branch_names" | xargs -n1 -P4 -I{} bash -c 'process_branch "$@"' _ {}
