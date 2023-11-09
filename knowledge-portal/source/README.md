# Knowlege portal Source Git

## Usage

### Adding this pipeline to your repo

You will have to modify the existing `gitlab-ci.yml` file to include:

```yaml
stages:
  - push 

include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/.gitlab-ci.yml'

variables:
  GIT_STRATEGY: clone

```
**Note: The pipeline can be added to any branch.** On `main`, it runs automatically and on other branches, it needs to be trigerred manually. 

### Connect your Source Git repository to the Knowledge Portal

Here is an example of a `docs-manifest.toml` file that you can use to create your own and connect your repository to knowledge portal:


```toml
# "includes" section maps paths inside your source Git repository to paths that the documents should take within the Knowledge Portal
# If a source path is a directory, all files with the .md extension within that directory (and its subdirectories) will be copied
# If a source path is a file, only that file will be copied
# Any folder mapping should end with '/'

[includes]
"my_folder/" = ["dkp-path/folder1/", "dkp-path/folder2/"] # Copies all .md files in the "my_folder" directory to both "dkp-path/folder1" and "dkp-path/folder2"
"my_folder/sub_folder/readme.md" = ["dkp-path/sub_folder/readme.md"] # Copies "my_folder/sub_folder/readme.md" to "dkp-path/sub_folder/readme.md"
"my_file.md" = ["dkp-path/new_file.md", "dkp-path/folder1/my_file.md"] # Copies "my_file.txt" to both "dkp-path/new_file.txt" and "dkp-path/folder1/my_file.txt"

# This section specifies files or directories to exclude from the copy process

[excludes]
exclude_files = ["excluded_folder/", "excluded_file.md"] # Excludes the "excluded_folder" directory and the "excluded_file.txt" file from being copied

```

> Image mappings for a markdown file get generated dynamically in the pipeline, and get copied over to Knowledge Portal. However, there are some conditions which are explained in section [source pipeline checks](#source-pipeline-checks) . 

## Additional Information

### Source Pipeline Checks

Before the job in pipeline pushes files to Knowledge Portal, it checks multiple things based on your mapping file. Knowing about these checks will help you setup the `docs-manifest.toml` file easily and make any necessary changes in your repository files.

- Ensure that the source path specified in the `includes` section exists.
- Ensure that any file being copied is less than 500KB in size.
- If a folder is specified in the `includes` or `excludes` sections (both source and destination), make sure to end the path with a forward slash `/`.
- Ensure that there are no spaces in the file paths (both source and destination) and image paths that are being copied to the Knowledge Portal.
- Check that only supported file types are being copied. Supported file types include `.md`, `.jpg`, `.png`, `.gif`, `.svg`, and `.ico`.
- Pipeline figures out the type of image path specified in a markdown file, and converts any relative image path to absolute path before copying over to Knowledge Portal. Any path starting with `http` will not be changed in the markdown file.

### Configure CI/CD variables

1. Go to `Settings >> CI/CD >> Variables`
2. Click on `Add variable`. 
3. Give the name `CENTRAL_GIT_PUSH_URL` in `Key` field and `Value` field will be provided by your maintainers.
    * For maintainers: The `CENTRAL_GIT_PUSH_URL` will be of the form: `https://oauth2:$BOT_ACCESS_TOKEN@gitlab.com/<org-name>/<path-to-central-git-repo>.git`
4. Click on `Add variable` button to confirm changes. 


> The steps of this section are being performed on the overall gitlab instance, so that it need not be replicated for every repo.
