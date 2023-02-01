# This script would take in a list of file names and find the reverse mappings after pipeline checks
# Assumptions:
# manifests/<repo_name>.txt: Source repo name should be the manifest name
# manifests have the convention: `source-->destination`

import sys
from glob import glob

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
        
        # Check if line contains "-->", if yes, strip the line at "-->" and get source and central paths 
        paths = {}  # central path as key and source path as value 
        for line in lines:
            if "-->" in line:
                central_path = line.split('-->')[1].strip()
                paths[central_path] = line.split('-->')[0]    
        
        # Iterate through RHS and see if we find any matches in changed files
        for central_path in paths.keys():  
            matches = [s for s in changed_files if central_path in s]
            if matches:
                source_path = ''.join(map(str, paths[central_path]))
                print(f"{repo_name}:{central_path}-->{source_path}")