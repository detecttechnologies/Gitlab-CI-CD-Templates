import sys
from glob import glob
import toml
import re
import os

changed_files = sys.argv[1:]

CHANGED_FILES = [file for file in changed_files if file.endswith(".md")] 
MANIFEST_LST = glob("manifests/*.toml")
FILESIZE_LIMIT = 500


def load_manifests(manifest_file):
    manifest_json = toml.load(manifest_file)
    mappings = manifest_json["includes"]
    return mappings

def get_repo_name(manifest_file):
    repo_name = manifest_file.split('/')[1]           # remove /manifests
    repo_name = repo_name.split('.')[0]               # remove .toml
    repo_name = repo_name.split('docs-manifest_')[1]  # remove docs-manifest_
    return repo_name

def get_md_file_paths(central_path):
    md_files = glob(os.path.join(central_path, "**/*.md"), recursive=True)
    return md_files


def get_updated_mappings(changed_files, mapppings):
    updated_mappings = {}
    for source_path, central_paths in mapppings.items():
        for central_path in central_paths:
            
            # Check if central path is a folder path 
            if not os.path.isdir(central_path):
                md_file_paths = []
            else:
                # From a folder path get all md file paths
                md_file_paths = get_md_file_paths(central_path)

            # Update the mapping json if folder paths are present 
            if md_file_paths:
                for md_file_path in md_file_paths:
                    if md_file_path in changed_files:
                        file_path = md_file_path.split(central_path)[1] # Gives you relative path from folder mapping defined in manifest
                        new_source_path = os.path.join(source_path, file_path) 
                        updated_mappings[md_file_path] = new_source_path
            else:
                if central_path in changed_files:
                    updated_mappings[central_path] = source_path
    return updated_mappings

def find_images(central_path):
    with open(central_path, "r") as f:
        content = f.read()
    image_regex = r"!\[.*\]\((.+)\)"
    images = re.findall(image_regex, content)
    updated_images = [image.strip() for image in images if not image.startswith("http")]
    return updated_images


def check_filesize(path):
    file_size = (os.stat(str(path)).st_size)/1000
    if file_size > FILESIZE_LIMIT:
        sys.exit(f"Error: {central_path} is too large to copy (>500KB). Current size: {file_size}.")
    else:
        return True

def normalize_path(path):
  
    # Split the path into components
    components = path.split('/')

    # Initialize an empty list to hold the normalized components
    normalized_components = []

    # Loop through the components and build the normalized path
    for component in components:
        # Ignore empty components and '.'
        if component == '' or component == '.':
            continue
        # Handle '..' by removing the last normalized component
        elif component == '..':
            if len(normalized_components) > 0:
                normalized_components.pop()
        # Add all other components to the normalized path
        else:
            normalized_components.append(component)

    # Join the normalized components and return the result
    normalized_path = '/'.join(normalized_components)
    return normalized_path


def create_image_mappings(updated_mappings):
    all_image_mappings = {}
    for central_path, source_path in updated_mappings.items():
        central_folder = os.path.dirname(central_path)
        source_folder = os.path.dirname(source_path)
        images = find_images(central_path)
        if images:
            # Create source and central image mappings
            image_mappings_array = []
            for central_image_path in images:
                image_mappings = {}
                if central_image_path.startswith("/"):
                    # rel_central and abs_central are assumed same in this case
                    abs_central_image_path = central_image_path[1:]
                    rel_central_image_path = abs_central_image_path
                    rel_path = os.path.relpath(rel_central_image_path, central_folder)
                    abs_source_image_path = os.path.join(source_folder, rel_path)
                    # normalize_path function helps in removing /../ or /./ present in entire path string
                    abs_source_image_path = normalize_path(abs_source_image_path)
                else:
                    rel_central_image_path = central_image_path
                    abs_central_image_path = os.path.join(central_folder, rel_central_image_path)
                    abs_central_image_path = normalize_path(abs_central_image_path)
                    abs_source_image_path = os.path.join(source_folder, rel_central_image_path)
                    abs_source_image_path = normalize_path(abs_source_image_path)

                # Check image filesize
                check_filesize(abs_central_image_path)
        
                image_mappings["rel_central"] = rel_central_image_path
                image_mappings["abs_central"] = abs_central_image_path
                image_mappings["abs_source"] = abs_source_image_path
                image_mappings_array.append(image_mappings)

            all_image_mappings[central_path] = image_mappings_array

    return all_image_mappings

def modify_image_paths(updated_mappings, all_image_mappings):
    for central_path, source_path in updated_mappings.items():
        image_mappings = all_image_mappings.get(central_path, [])
        if image_mappings:
            with open(central_path, "r") as f:
                content = f.read()
            for image_mapping in image_mappings:
                original = image_mapping["rel_central"]
                new = image_mapping["abs_source"]
                    
                if original == image_mapping["abs_central"]:
                    content = content.replace(original, new)
                else:
                    # if rel_path and abs_path are not same add a '/' in central_image_path. In other case, it's already there in file.
                    content = content.replace(original, f"/{new}")
            with open(central_path, "w") as f:
                f.write(content)
    return True


# Load all manifests and get file_mapppings and image_mappings one by one
for manifest_file in MANIFEST_LST:
    mappings = load_manifests(manifest_file)

    # Get repository name for this manifest file
    repo_name = get_repo_name(manifest_file) 

    # Check if changed file path exists in central paths of file mappings
    updated_mappings = get_updated_mappings(CHANGED_FILES, mappings)

    # Get all image mappings for updated mappings which are also valid mappings for this commit if they exist
    if updated_mappings:
        all_image_mappings = create_image_mappings(updated_mappings)
        modify_image_paths(updated_mappings, all_image_mappings)

        # Print to bash output
        for central_path, source_path in updated_mappings.items():
            print(f"{repo_name}:{central_path}-->{source_path}")    
        
            image_mappings = all_image_mappings.get(central_path, [])
            for image_mapping in image_mappings:
                central_image = image_mapping["abs_central"]
                source_image = image_mapping["abs_source"]
                print(f"{repo_name}:{central_image}-->{source_image}")
