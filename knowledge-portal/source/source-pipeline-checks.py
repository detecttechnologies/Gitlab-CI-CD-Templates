import os
import sys
from glob import glob
import toml
import re
import shutil

MANIFEST_FILE = "docs-manifest.toml"
FILESIZE_LIMIT = 500
SUPPORTED_FILE_TYPES = (".md", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico")

def load_manifest(manifest_file):
    manifest_json = toml.load(manifest_file)
    mappings = manifest_json["includes"]
    exclude_files = manifest_json["excludes"]["exclude_files"]
    return mappings, exclude_files

def get_md_file_paths(source_path):
    md_files = glob(os.path.join(source_path, "**/*.md"), recursive=True)
    return md_files

def is_valid_path(source_path):
    if not os.path.exists(source_path):
        sys.exit(f"Error: {source_path} doesn't exist")
    elif not source_path.endswith(SUPPORTED_FILE_TYPES) and not os.path.isdir(source_path):
        sys.exit(f"Error: {source_path} is an unsupported file type.")
    elif os.path.isdir(source_path) and not source_path.endswith("/"):
        sys.exit(f"Error: For {source_path}, mapping should end with / as it is a folder mapping.")
    else:
        return True

def check_central_path(central_paths):
    for central_path in central_paths:
        if not central_path.endswith("/") and os.path.isdir(central_path):
            sys.exit(f"Error: {central_path} in central should end with / as it is a folder mapping.")
        # This condition becomes true if central path mentioned is root directory of central repo
        if not os.path.dirname(central_path):
            sys.exit(f"Error: You can't create a path directly, {central_path}, to the root of the central repo.")
    return True

def check_filesize(source_path):
    file_size = (os.stat(str(source_path)).st_size)/1000
    if file_size > FILESIZE_LIMIT:
        sys.exit(f"Error: {source_path} is too large to copy (>500KB). Current size: {file_size}.")
    else:
        return True

def check_spaces(path):
    if " " in path:
        sys.exit(f"Error: {path} contains spaces. Wikijs doesn't allow us to sync files with spaces. Rename your file.")
    else:
        return True

def find_images(source_path):
    with open(source_path, "r") as f:
        content = f.read()
    image_regex = r"!\[.*\]\((.+)\)"
    images = re.findall(image_regex, content)
    updated_images = [image.strip() for image in images if not image.startswith("http")]
    return updated_images

def perform_basic_checks(mappings):
    # Get updated mappings that pass the following checks
    updated_mappings = {}
    for source_path, central_paths in mappings.items():
        
        # Check if source path is valid
        if is_valid_path(source_path):
            # Check if source path is a folder path 
            if not os.path.isdir(source_path):
                md_file_paths = []
            else:
                # From a folder path get all md file paths
                md_file_paths = get_md_file_paths(source_path)

            # Central path checks
            check_central_path(central_paths)
                    
            # Update the mapping json if folder paths are present 
            if md_file_paths:
                for md_file in md_file_paths:
                    new_source_path = md_file
                    new_central_paths = [] 
                    file_path = md_file.split(source_path)[1]
                    for central_path in central_paths:
                        new_central_paths.append(f"{central_path}{file_path}")  
                    updated_mappings[new_source_path] = new_central_paths
            else:
                updated_mappings[source_path] = central_paths
    return updated_mappings

def perform_exclude_checks(updated_mappings):
    # Update mappings after checking excludes
    for exclude_path in exclude_files:
        if is_valid_path(exclude_path):
            if not os.path.isdir(exclude_path):
                if exclude_path in updated_mappings.keys():
                    del updated_mappings[exclude_path]
            else:
                md_file_paths = get_md_file_paths(exclude_path)
                for md_file in md_file_paths:
                    if md_file in updated_mappings.keys():
                        del updated_mappings[md_file]
    return updated_mappings

def perform_additional_checks(updated_mappings):
    # Additional checks: Filesize and spaces in updated mappings
    for source_path, central_paths in updated_mappings.items():
        # Source checks
        # check_filesize(source_path)
        check_spaces(source_path)
        # Central checks
        for central_path in central_paths:
            check_spaces(central_path)
    return updated_mappings

def copy_updated_mappings(updated_mappings):
    for source_path, central_paths in updated_mappings.items():
        for central_path in central_paths:
            central_path_folder = os.path.dirname(central_path)
            os.makedirs(f"/root/central/{central_path_folder}", exist_ok=True)
            shutil.copy(source_path, f"/root/central/{central_path}")
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
    for source_path, central_paths in updated_mappings.items():
        source_folder = os.path.dirname(source_path)
        # Find all images for a source path
        images = find_images(source_path)
        if images:
            for central_path in central_paths:
                image_mappings_array = []
                central_folder = os.path.dirname(central_path)
                for source_image_path in images:
                    image_mappings = {}
                    # If path is absolute, use relapth() to find the relative position of image from markdown file
                    if source_image_path.startswith("/"):
                        # rel_source and abs_source are assumed same in this case
                        abs_source_image_path = source_image_path[1:]
                        rel_source_image_path = abs_source_image_path
                        rel_path = os.path.relpath(rel_source_image_path, source_folder)
                        abs_central_image_path = os.path.join(central_folder, rel_path)
                        # normalize_path function helps in removing /../ or /./ present in entire path string
                        abs_central_image_path = normalize_path(abs_central_image_path)
                    else:
                        rel_source_image_path = source_image_path
                        abs_source_image_path = os.path.join(source_folder, rel_source_image_path)
                        abs_source_image_path = normalize_path(abs_source_image_path)
                        abs_central_image_path = os.path.join(central_folder, rel_source_image_path)
                        abs_central_image_path = normalize_path(abs_central_image_path)
                    
                    check_filesize(abs_source_image_path)

                    image_mappings["rel_source"] = rel_source_image_path
                    image_mappings["abs_source"] = abs_source_image_path
                    image_mappings["abs_central"] = abs_central_image_path
                    image_mappings_array.append(image_mappings)

                all_image_mappings[central_path] = image_mappings_array
    return all_image_mappings    

def copy_image_mappings(all_image_mappings):
    central_paths = all_image_mappings.keys()
    for central_path in central_paths:
        image_mappings = all_image_mappings[central_path]
        for image_mapping in image_mappings:
            source_image_path = image_mapping["abs_source"]
            central_image_path = image_mapping["abs_central"]
            central_folder = os.path.dirname(central_image_path)
            os.makedirs(f"/root/central/{central_folder}", exist_ok=True)  
            shutil.copy(source_image_path, f"/root/central/{central_image_path}")     
    return True

def modify_image_paths(updated_mappings, all_image_mappings):
    for source_path, central_paths in updated_mappings.items():
        for central_path in central_paths:
            image_mappings = all_image_mappings.get(central_path, [])
            if image_mappings:
                with open(f"/root/central/{central_path}", "r") as f:
                    content = f.read()
                for image_mapping in image_mappings:
                    original = image_mapping["rel_source"]
                    new = image_mapping["abs_central"]
                      
                    if original == image_mapping["abs_source"]:
                        content = content.replace(original, new)
                    else:
                        # if rel_path and abs_path are not same add a '/' in central_image_path. In other case, it's already there in file.
                        content = content.replace(original, f"/{new}")
                with open(f"/root/central/{central_path}", "w") as f:
                    f.write(content)
    return True

# Load the contents from manifest file
mappings, exclude_files = load_manifest(MANIFEST_FILE)

# Perform basic checks and get updated mappings
updated_mappings = perform_basic_checks(mappings)

# Perform checks based on exclude section of .toml
updated_mappings = perform_exclude_checks(updated_mappings)

# Perform additional checks and get updated mappings
perform_additional_checks(updated_mappings)

# Copy updated mappings to respective path in /root/central before changing image paths
copy_updated_mappings(updated_mappings)

# Create image mappings 
all_image_mappings = create_image_mappings(updated_mappings)

# Copy all image mappings to respective path in /root/central
copy_image_mappings(all_image_mappings)

# Modify image paths for .md files in /root/central
modify_image_paths(updated_mappings, all_image_mappings)
