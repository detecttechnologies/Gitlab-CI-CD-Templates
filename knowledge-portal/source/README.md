# Usage

## Adding this pipeline to your repo

You will have to modify the existing `gitlab-ci.yml` file to include:

```yaml
    stages:
        - copy_to central_repo
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/.gitlab-ci.yml'

```
## Configure CI/CD variables

1. Go to `Settings >> CI/CD >> Variables`
2. Click on `Add variable`. 
3. Give the name `PUSH_TOKEN` in `Key` field and `Value` field will be provided by Platform Team.
4. Click on `Add variable` button to confirm changes. 

## Creating `manifest.txt` file

- The manifest file keeps track of README files you choose to import to `central-repo`.
- It also allows renaming a file and import copies of same file to separate destination folders.   
- The `manifest.txt` file should be created at the root of your repository.

An example of a `manifest.txt` file is added below:

```txt
README.md-->Platform/CI-CD-Pipelines/wikijs-demo-pipeline/demo-source/folder1/folder3/hello.md
README.md-->Platform/CI-CD-Pipelines/wikijs-demo-pipeline/demo-source/folder2/README.md
fol1/read.md-->Platform/CI-CD-Pipelines/wikijs-demo-pipeline/demo-source/folder2/read.md
```
>where, `Platform/CI-CD-Pipelines/wikijs-demo-pipeline/demo-source/` added to RHS of each line represents a substring of the entire repo path **gitlab.com/DetectTechnologies/`Platform/CI-CD-Pipelines/wikijs-demo-pipeline/`demo-source.git** in which the manifest file will be saved 


