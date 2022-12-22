# This script would take in a list of file names and find the reverse mappings
# Assumptions:
# manifests/<repo_name>.txt: Source repo name should be the manifest name
# manifests have the convention: `source-->destination`
import os
import subprocess
import sys
import time
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
