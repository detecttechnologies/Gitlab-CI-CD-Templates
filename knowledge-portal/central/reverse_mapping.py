# This script would take in a list of file names and find the reverse mappings
# Assumptions:
# manifests/<repo_name>.txt: Source repo name should be the manifest name
# manifests have the convention: `source-->destination`
import os
import subprocess
import sys
import time
from glob import glob


def sp_run(s):
    # Takes a string with spaces and splits it into lst
    return subprocess.run(s.split())

changed_files = sys.argv[1:]
manifests_lst = glob("manifests/*.txt")

for manifest in manifests_lst:
    # Key-value store with schema repo_name:[changed_files]
    mappings = {}

    # remove /manifests
    repo_name = manifest.split('/')[1]

    # remove .txt
    repo_name = repo_name.split('.')[0]

    # remove docs-manifest_
    repo_name = repo_name.split('docs-manifest_')[1]
    
    with open(manifest, 'r') as f:

        # Get all lines in the manifest as a list
        lines = f.readlines()

        # Split by '-->', take RHS and strip white spaces
        rhs_lines = [s.split('-->')[1].strip() for s in lines]
        
        # Iterate through rhs_lines and get lhs_lines for them with rhs as key and lhs as value
        lhs_lines = {}
        for rhs_line in rhs_lines:
            lhs_lines[rhs_line] = [s.split('-->')[0] for s in lines if s.split('-->')[1].strip() == rhs_line]

        # Iterate through RHS and see if we find any matches in changed files
        for rhs_line in rhs_lines:
            if rhs_line in changed_files:
                lhs_line = ''.join(map(str, lhs_lines[rhs_line]))
                print(f"{repo_name}:{rhs_line}-->{lhs_line}")

# if mappings:
        #     # clone the repo from repo_name
            
        #     sp_run(f'git clone -v https://oauth2:{BOT_ACCESS_TOKEN}@gitlab.com/DetectTechnologies/{source_repo_path}.git /root/source/{source_repo_nopath}')

        #     # create knowledge-portal_changes branch
        #     mycwd = os.getcwd()
        #     os.chdir(f'/root/source/{source_repo_nopath}')
        #     sp_run('git checkout -B knowledge-portal_changes')
        #     os.chdir(mycwd)
    
        #     # copy files
        #     for rhs_line in mappings[repo_name]:
        #         lhs_line = ''.join(map(str, lhs_lines[rhs_line]))
        #         print(f'LHS Line: {lhs_line}')
        #         print(f'RHS Line: {rhs_line}')
        #         sp_run(f'ls -al /root/source/{source_repo_nopath}')
        #         # remove lhs_file from repo before copying new file

        #         sp_run(f'rm -rfv /root/source/{source_repo_nopath}/{lhs_line}')
        #         sp_run(f'cp -v ./{rhs_line} /root/source/{source_repo_nopath}/{lhs_line}')
        #         # sp_run("echo $(find . -wholename '*{rhs_line}*')")

        #         # cmd = f"for file in $(find . -wholename '*{rhs_line}*');do cp -rf -v $file /root/source/{lhs_line};done;"
        #         sp_run(f'ls -al /root/source/{source_repo_nopath}')
        #         mycwd = os.getcwd()
        #         os.chdir(f'/root/source/{source_repo_nopath}')
        #         sp_run('git status')
        #         os.chdir(mycwd)

        #     # Create MR and push to branch
        #     mycwd = os.getcwd()
        #     os.chdir(f'/root/source/{source_repo_nopath}')
        #     sp_run('git branch')
        #     # sp_run(f'curl --header "https://oauth2:{MERGE_REQUEST_TOKEN}gitlabhost.com/api/v4/merge_requests?scope=all&state=opened"')
        #     sp_run('git add -A')
        #     sp_run('git commit -m doc-update-from-knowledge-portal')
        #     sp_run(f'git push -f -o merge_request.create -o merge_request.draft -o merge_request.title="doc-update-from-knowledge-portal" -o merge_request.target=main https://oauth2:{BOT_ACCESS_TOKEN}@gitlab.com/DetectTechnologies/{source_repo}.git knowledge-portal_changes')
        #     os.chdir(mycwd)
