#!/bin/bash

# changed files can be obtained by git diff between latest commit and unstaged area
changed_files=$(git diff --name-only HEAD);
echo "Files changed in knowledge portal: ${changed_files}";

if [[ $changed_files ]]
then
    # Reverse the git reset and move files to staged as we will need latest files 
    git add -A && git commit -m "docs:reversing soft reset as now we have the filenames"

    # Run python script to get output in format "source_repo_name:filepath_central_gitrepo-->filepath_source_gitrepo"
    output=$(python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/central/reverse_mapping.py)" $changed_files)
    
    # Create an array to keep track of all unique source repos in which files have been modified
    declare -a source_repo_array

    # From python output, separate line to corresponding variables 
    while read line 
    do
        split_output=(${line//":"/ })
        source_repo_name=${split_output[0]}
        split_mapping=(${split_output[1]//"-->"/ })
        lhs_path=${split_mapping[1]}
        rhs_path=${split_mapping[0]}
        echo "lhs_path:${lhs_path}, rhs_path:${rhs_path}, source_repo_name:${source_repo_name}"

        # Create a unique directory for each source repo and copy files
        unique_directory="/root/source/${source_repo_name}"
        
        # Get source_repo_path by changing '_' to '/'
        source_repo_path=${source_repo_name//'_'/'/'} 
        
        if [ -d "$unique_directory" ]
        then
            # Remove existing and Copy changed files to unique_directory
            rm -rfv ${unique_directory}/${lhs_path}
            cp -v ./${rhs_path} ${unique_directory}/${lhs_path}
        else
            # Create directory, clone source repo, create branch, and initiate copy
            mkdir -p ${unique_directory}
            source_repo_array+=( "${source_repo_name}" )
            git clone -v https://oauth2:${BOT_ACCESS_TOKEN}@gitlab.com/DetectTechnologies/${source_repo_path}.git ${unique_directory}
            cd ${unique_directory}
            git checkout -B knowledge-portal_changes
            cd -
            rm -rfv ${unique_directory}/${lhs_path}
            cp -v ./${rhs_path} ${unique_directory}/${lhs_path}
        fi
    done <<< ${output} 
    echo "Done"
    
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
    echo "Done"
else
    echo "This is not a commit that happened through knowledge portal"
fi
