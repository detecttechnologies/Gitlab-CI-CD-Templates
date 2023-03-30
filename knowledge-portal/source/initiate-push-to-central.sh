#!/bin/bash

set -e

# Set credentials
git config --global user.email "PlatformTeam@detecttechnologies.com"
git config --global user.name "Detect Gitlab Bot"
git clone $CENTRAL_GIT_PUSH_URL /root/central

# Run python script for pipeline checks and copy mappings to /root/central
python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/source-pipeline-checks.py)"
echo "Done! Copied mappings to /root/central."

# Extract the unique path (Subpath) from Repository url      
unique_path_temp1=(${CI_REPOSITORY_URL//"gitlab.com/"/ })           # split after 'gitlab.com/' 
unique_path_temp2=(${unique_path_temp1[1]//"."/ })                  # split before .git
unique_path="$( cut -d '/' -f 2- <<< "${unique_path_temp2[0]}" )"   # split after first '/'
manifest_suffix=${unique_path//"/"/_}
echo "Done! source-repo's path: ${unique_path}, manifest suffix: ${manifest_suffix}"

# Copy the source-git's manifest to central-git by adding source-path in manifest filename
mkdir -p /root/central/manifests
cp -v docs-manifest.toml /root/central/manifests/docs-manifest_${manifest_suffix}.toml
echo "Done! Copied manifest file to /root/central."

# Push back to central-git with the updated changes
cd /root/central
git add -A 
# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Commit in source pipeline for ${unique_path}"
    git push origin HEAD:main -f;
    echo "Done! Pushed files to central git."
else
    echo "Done! No changes to commit."
fi
