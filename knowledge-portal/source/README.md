# Usage

## Adding this pipeline to your repo

You will have to modify the existing `gitlab-ci.yml` file to include:

```yaml
    stages:
        - push
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/.gitlab-ci.yml'

```
## Configure CI/CD variables

1. Go to `Settings >> CI/CD >> Variables`
2. Click on `Add variable`. 
3. Give the name `CENTRAL_GIT_PUSH_URL` in `Key` field and `Value` field will be provided by your maintainers.
    * For maintainers: The `CENTRAL_GIT_PUSH_URL` will be of the form: `https://oauth2:$PUSH_TOKEN@gitlab.com/<org-name>/<path-to-central-git-repo>.git`
4. Click on `Add variable` button to confirm changes. 


> Ideally the steps of this section can be performed on the overall gitlab instance, so that it need not be replicated for every repo.

## Creating `manifest.txt` file

- The manifest file keeps track of files you choose to import to `central-repo`.
- It also allows renaming a file and copying the same file to separate destination folders in case you would like to have different views of the same underlying data through force-duplication.
- The `docs-manifest.txt` file should be created at the root of your project's repository.

An example of a `docs-manifest.txt` file is added below:
```txt
README.md-->my/prefix/folder1/folder3/hello.md
README.md-->my/prefix/folder2/README.md
fol1/read.md-->my/prefix/folder2/read.md
fol2/-->/
```
Notes:
1. `my/prefix/` is added to RHS of each line: represents a substring of the entire repo path **gitlab.com/<org_namespace>/`my/prefix/`source-repo.git** in which the manifest file will be saved
2. The last line in the sample above (`fol2/-->/`) shows how a folder can be copied as-is to the destination repo
