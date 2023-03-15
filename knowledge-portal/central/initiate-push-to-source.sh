#!/bin/bash

set -e

# Set credentials
git config --global user.email "PlatformTeam@detecttechnologies.com"
git config --global user.name "Detect Gitlab Bot"

# changed files can be obtained by git diff between latest commit and unstaged area
git reset --soft HEAD~1
changed_files=$(git diff --name-only HEAD)

if [[ $changed_files ]]
then
    echo "Files changed in knowledge portal: ${changed_files}"
    # Reverse the git reset and move files to staged as we will need latest files 
    git add -A && git commit -m "docs:reversing soft reset as now we have the filenames"

    # Run python script to get output in format "source_repo_name:filepath_central_gitrepo-->filepath_source_gitrepo"
    output=$(python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/central/central-pipeline-checks.py)" $changed_files)
    
    # Create an array to keep track of all unique source repos in which files have been modified
    declare -a source_repo_array

    # From python output, separate line to corresponding variables 
    while read line 
    do
        if [ "$line" ]
        then
            split_output=(${line//":"/ })
            source_repo_name=${split_output[0]}
            split_mapping=(${split_output[1]//"-->"/ })
            source_path=${split_mapping[1]}
            central_path=${split_mapping[0]}
            echo "source_path:${source_path}, central_path:${central_path}, source_repo_name:${source_repo_name}"

            # Create a unique directory for each source repo and copy files
            unique_directory="/root/source/${source_repo_name}"
            
            # Get source_repo_path by changing '_' to '/'
            source_repo_path=${source_repo_name//'_'/'/'} 
            
            if [ -d "$unique_directory" ]
            then
                # Remove existing and Copy changed files to unique_directory
                source_path_dir=$(dirname "${source_path}")
                mkdir -pv ${unique_directory}/${source_path_dir}
                cp -v ${central_path} ${unique_directory}/${source_path}
            else
                # Create directory, clone source repo, create branch, and initiate copy
                mkdir -p ${unique_directory}
                source_repo_array+=( "${source_repo_name}" )
                git clone -v https://oauth2:${BOT_ACCESS_TOKEN}@gitlab.com/DetectTechnologies/${source_repo_path}.git ${unique_directory}
                cd ${unique_directory}
                git checkout -B knowledge-portal_changes
                cd -
                source_path_dir=$(dirname "${source_path}")
                mkdir -pv ${unique_directory}/${source_path_dir}
                cp -v ${central_path} ${unique_directory}/${source_path}
            fi
        else
            echo "This is not a markdown file change scenario."
        fi
    done <<< ${output} 
    echo "Done. Copied all files."
    
    # Push all changes to source repos and create merge requests
    for source_repo in "${source_repo_array[@]}"
    do
        echo "Pushing to ${source_repo} and Creating a draft MR"
        source_repo_path=${source_repo//'_'/'/'}
        cd /root/source/${source_repo}
        git add -A && git commit -m "doc update from knowledge portal"
        git push -f -o merge_request.create -o merge_request.draft -o merge_request.title="doc update from knowledge portal" -o merge_request.target=main https://oauth2:${BOT_ACCESS_TOKEN}@gitlab.com/DetectTechnologies/${source_repo_path}.git knowledge-portal_changes
        cd -
    done
fi