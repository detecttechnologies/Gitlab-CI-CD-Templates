#!/bin/bash

set -e

# Run python script for pipeline checks and get mappings if all is well
output=$(python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/source-pipeline-checks.py)")
echo "Done, Mappings: ${output}"

# Extract the unique path (Subpath) from Repository url      
unique_path_temp1=(${CI_REPOSITORY_URL//"gitlab.com/"/ })           # split after 'gitlab.com/' 
unique_path_temp2=(${unique_path_temp1[1]//"."/ })                  # split before .git
unique_path="$( cut -d '/' -f 2- <<< "${unique_path_temp2[0]}" )"   # split after first '/'
manifest_suffix=${unique_path//"/"/_}
echo "Done, source-repo's path: ${unique_path}, manifest suffix: ${manifest_suffix}"

# Clone the destination repo, copy the source-git's manifest to central-git by adding source-path in manifest filename
git clone $CENTRAL_GIT_PUSH_URL /root/central
mkdir -p /root/central/manifests
cp -v docs-manifest.txt /root/central/manifests/docs-manifest_${manifest_suffix}.txt
echo "Done, Copied manifest file to central."

# Read all mappings from output and copy accordingly 
while read line
do
    if [[ "$line" == *"-->"* ]]
    then
        source_path="${line%-->*}"
        central_path="${line##*-->}"
        if [[ "$central_path" == *"/"* ]]
        then
            echo "${central_path}"
            path="${central_path%/*}"
            file="${central_path##*/}"
            mkdir -p -v /root/central/${path}
            cp -v ${source_path} /root/central/${path}/${file}
        else
            cp -v ${source_path} /root/central/${central_path}
        fi
    fi
done <<< ${output} 
echo "Done. Copied all files to central"

# Push back to central-git with the updated changes
cd /root/central
git config --global user.email "PlatformTeam@detecttechnologies.com"
git config --global user.name "Detect Gitlab Bot"
git add -A && git commit -m "Commit in source pipeline for ${unique_path}" --allow-empty;
git push origin HEAD:main -f;
echo "Done finally. Pushed files to central git."

