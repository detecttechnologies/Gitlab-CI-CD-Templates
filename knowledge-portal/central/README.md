# Knowledge Portal Central Pipeline

## Usage

### Adding this pipeline to your repo

You will have to modify the existing `gitlab-ci.yml` file to include:

```yaml
stages:
  - push

include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/central/.gitlab-ci.yml'

variables: 
  GIT_STRATEGY: clone

```

### Central Pipeline Checks

Before the job in pipeline pushes files back to `source`, it checks multiple things based on your mapping file. Knowing about these checks will help you use the pipeline easily and make any necessary changes before any change on wikijs become available at `source` repository.

- The jobs will only run when a commit happens on `main` branch with a message starting with `docs:`, This ensures that the jobs will only run when a commit has been made from wikijs portal.
- Ensure that all image URL paths in Markdown files are absolute and begin with `/`.
- Ensure all image URL paths in a Markdown file are in downstream of that Markdown file. 
- Ensure that any file being copied is less than 500KB in size.

## Use Cases: Changes on Knowledge Portal

If you adhere to checks performed by **Central Pipeline**, you can use the pipeline for following use cases:

### Uploading/Deleting an image on Knowldge Portal

- The pipeline will run as a new commit will happen at `central` with a commit message starting with `docs:`
- Since, no Markdown files have been changed since last commit, the pipeline will succed with a message "**This is not a markdown file change scenario.**"

### Creating a new Markdown file on Knowldge Portal

- If the Markdown file has been created inside a folder which exists in central mapping of `docs-manifest.toml` file, the file will be made available at the `source` as well in the MR that will get created once Knowledge Portal syncs with `central`.
- In case of new images in the markdown file,the new image will be made available at `source` with a modified absolute path in `source` repository.

### Deleting a Markdown file on Knowldge Portal

- If the file that has been deleted is part of any `source` repository
    - the files will get deleted on wikijs and in turn on `central` repository.
    - the pipeline however is not configured to deal with such situations,
        - so, the change won't sync back to source, and the pipeline will succed with a message "**This is not a markdown file change scenario.**".
        - if the file still exists at source, it will become available at   `central` and in turn on `Knowldge Portal` again, when the pipeline on `source` runs.  

## Edge Cases

1. Handling duplicates of the same file in different locations at `central`, with simultaneous modifications
    - If the same file exists in multiple locations (duplicates) at `central`, and both files are modified at the same time, the file mentioned later in the `docs-manifest` file (i.e., `duplicate2`) will take precedence and be pushed back to the `source` repository as the truth.
    - After the merge request (MR) is accepted at `source`, the pipeline will run again, and the contents of `duplicate2` will replace the contents of `duplicate1`.

2. Modifying files from multiple repositories simultaneously
    - Since the RHS (right-hand side) of `docs-manifest.toml` is unique, we can identify the source repository to which the file belongs based on the suffix (<repo_name>) present in `docs-manifest_<repo_name>.toml`.
    - We then clone those repos in unique folders, commit our changes, and push them to `source` repository.
