#!/bin/bash

# Setup Credentials
git config --global user.email "PlatformTeam@detecttechnologies.com"
git config --global user.name "Detect Gitlab Bot"

# Copy files from artifacts to their original distination and remove artifacts folder
cwd=$(pwd)
cd artifacts
find . -name "**" -exec cp -R --parents \{\} $cwd/ \;
cd -
rm -rf artifacts

# Clone destination repo to make it available as local inside pipeline
git clone "https://oauth2:$BOT_ACCESS_TOKEN@gitlab.com/${BUILD_OUTPUT_REPO}" /root/dest

# Remove branches from remote if the variable is assigned "true"
cd /root/dest
if [[ $REMOVE_BRANCHES == "true" ]]
then
    git branch -r | awk -F/ '/\/linux/{print $2}' | xargs -I {} git push origin :{};
fi
cd -

# Setup a branch for every unique deployment footprint, push to each of them
# Find all py and arch version combinations, use them as branches

branch_names=$(find . -wholename "**/*.so" | sort -u | head -20 | awk -F '-' '{print $(NF-1)"-"$(NF-2)"-py"$(NF-3)}' | sort -u)
echo "Branches to be pushed: ${branch_names}"

for branch in ${branch_names}
do  
    echo "-------------------------------------------"
    echo "Now pushing branch ${branch}"
    cd /root/dest
    
    # Switch to the branch (create if it doesn't exist)
    git checkout --quiet ${branch} 2>/dev/null || git checkout -b ${branch}

    #Delete all files before pushing if any
    git rm -rf * || true
    git commit -m "removing previous builds" || true
    git push --quiet origin HEAD:${branch} -f || true
    cd -
    
    # From the build folder, copy the new .so files, main.py and all __init__.py's;
    
    file_name_pattern=$(echo ${branch} | awk -F '-' '{print $3"-"$2"-"$1}') # Undo the reversing carried out while forming the branch_name
    file_name_pattern=${file_name_pattern:2}   # Remove the 'py' at the start;
    find . -wholename "**/*${file_name_pattern}*.so" ! -wholename "./iva.**.so" -exec cp --parents \{\} /root/dest/ \;
    cp ./main.py /root/dest/ || true
    find . -wholename "**/__init__.py" -exec cp --parents \{\} /root/dest/ \;

    # IVA repo specific code
    cp ./iva.py /root/dest/ || true

    # From the build folder, copy the files and folders mentioned in variable "COPY_FILES" while ignoring .py and .so files;
    for file in ${COPY_FILES}
    do
        if [[ "$file" == *"-->"* ]]
        then
            split=(${file//-->/ })
            echo "${split[0]}"
            echo "${split[1]}"
            cp -R -v ${split[0]} /root/dest/${split[1]}
        else
            find . -type f -wholename "*$file*" ! -wholename "./*.so" ! -wholename "./*.py" -exec cp -v -R --parents \{\} /root/dest/ \;
        fi
    done

    #Rename filenames to original names
    cd /root/dest
    for f in $(find . -type f -wholename "./**.so") 
    do
        mv -v "$f" "${f/.cpython-${file_name_pattern}-gnu./.}" || mv -v "$f" "${f/.cpython-${file_name_pattern}-gnueabihf./.}"
    done
    cd -

    # Get timestamp of last commit from source repo
    timestamp=$(git log -1 --format=%cd --date=local)

    # Push back the updated repository
    cd /root/dest
    
    git add -A && git commit -m "Commit in source pipeline at timestamp:$timestamp" --allow-empty
    git reflog expire --expire-unreachable=now --all
    git gc --prune=now
    
    # Merge all commits in one
    git reset $(git commit-tree HEAD^{tree} -m "Commit in source pipeline at timestamp:$timestamp")
    git push --quiet origin HEAD:${branch} -f
    
    cd - # Switch back to the source repo before the next iteration
    done
