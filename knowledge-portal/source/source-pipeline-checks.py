import os
import sys
from glob import glob

# Max filesize to be copied over to central
FILESIZE_LIMIT = 500

# Check if folder copy scenario; if yes, get all files in the folder recursively
def check_for_folders(source_paths):
    folder_mappings = {}
    # Folder mappings expanded to their corresponding recursive file mappings
    for source_path in source_paths:
        # Check if source_path is a folder
        if os.path.exists(source_path):
            if os.path.isdir(source_path):
                if source_path.endswith("/"):
                    mycwd = os.getcwd()
                    os.chdir(source_path)
                    files = glob('**/*.*', recursive=True)
                    os.chdir(mycwd)
                    folder_mappings[source_path] = files
                else:
                    sys.exit(f"Check failed! This folder: {source_path} path doesn't end with (/)")
        else:
            sys.exit(f"Check failed! This file/folder: {source_path} mentioned in manifest file doesn't exist or you have not ended your folder copy with (/)")
    return folder_mappings


# source files to delete before copying
def remove_paths(mappings, source_paths_to_remove):
    
    current_source_paths = list(mappings.values())
    folder_mappings = check_for_folders(current_source_paths)
   
   # Update mappings: file-->file mapping from folder
    for source_path in list(folder_mappings.keys()):
        central_paths = [i for i in mappings if mappings[i]==source_path]
        for central_path in central_paths:
            for file in folder_mappings[source_path]:
                mappings[f"{central_path}{file}"] = f"{source_path}{file}"
            del mappings[central_path]
    # Update mappings by deleting keys mentioned in source_paths to remove
    for source_path in source_paths_to_remove:
        if source_path in list(mappings.values()):
            central_paths = [i for i in mappings if mappings[i]==source_path]
            if central_path:
                for central_path in central_paths:
                    del mappings[central_path]
    return mappings

# Check for spaces in mappings
def check_for_spaces(mappings):
    mappings_with_spaces = {}
    for mapping in list(mappings.keys()):
        if " " in mapping or " " in mappings[mapping]:
            mappings_with_spaces[mapping] = mappings[mapping]
    if mappings_with_spaces:
        sys.exit(f"Check failed! Mappings have spaces: {mappings_with_spaces}")
    else:
        return mappings

# Check filsize for source mappings 
def check_filesize(mappings, size):
    source_paths = list(mappings.values())
    for source_path in source_paths:
        if source_path.startswith("/"):
            source_path = source_path.split("/")[1:]
            source_path = "/".join(source_path)
        file_size = (os.stat(source_path).st_size)/1000
        if file_size > size:
            sys.exit(f"Check failed: {source_path} is too large to copy (>500KB). Current size: {file_size}.")
    return mappings

with open("docs-manifest.txt", 'r') as f:
    lines = f.readlines()

    # Get all lines with '!' pattern
    lines_with_exclamation = [line.strip() for line in lines if "!" in line]

    # Get all lines with '-->' pattern 
    lines_with_arrows = [line.strip() for line in lines if "-->" in line]
        
    # Get source and central paths as key:value pair
    # central is key and source is value as central mappings are unique
    mappings = {}
    for line in lines_with_arrows: 
        mappings[line.split('-->')[1].strip()] = line.split('-->')[0].strip()
    
    # Get source paths to be removed before coying
    source_paths_to_remove = [line.split('!')[1].strip() for line in lines_with_exclamation]

    # Check if folders are mentioned in source paths to remove; Convert to file mapping 
    folder_mappings_to_delete = check_for_folders(source_paths_to_remove)
    
    # Update source paths to delete list: Add file paths and remove folder path
    for key in folder_mappings_to_delete.keys():
        files = [f"{key}{file}" for file in folder_mappings_to_delete[key]]
        source_paths_to_remove.extend(files)
        source_paths_to_remove.remove(key)
    
    # Update mappings based on source_paths_to_remove
    mappings = remove_paths(mappings, source_paths_to_remove)
    
    # Check if mappings have spaces
    mappings = check_for_spaces(mappings)

    # Check if filesize of a mapping is >500KB
    mappings = check_filesize(mappings, FILESIZE_LIMIT)

    # Write to bash output variable if all checks pass
    mapping_array = []
    for mapping in mappings.keys(): 
        mapping_array.append(f"{mappings[mapping]}-->{mapping}") 

    # Print to stdout
    for mapping in mapping_array:
        print(mapping)
    
