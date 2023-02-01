# Usage

## Adding this pipeline to your repo

You will have to modify the existing `gitlab-ci.yml` file to include:

```yaml
    stages:
        - push
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/source/.gitlab-ci.yml'

```
## Configure CI/CD variables (applied on overall gitlab instance)

1. Go to `Settings >> CI/CD >> Variables`
2. Click on `Add variable`. 
3. Give the name `CENTRAL_GIT_PUSH_URL` in `Key` field and `Value` field will be provided by your maintainers.
    * For maintainers: The `CENTRAL_GIT_PUSH_URL` will be of the form: `https://oauth2:$PUSH_TOKEN@gitlab.com/<org-name>/<path-to-central-git-repo>.git`
4. Click on `Add variable` button to confirm changes. 


> The steps of this section are being performed on the overall gitlab instance, so that it need not be replicated for every repo.

## Creating `manifest.txt` file

- The manifest file keeps track of files you choose to import to `central-repo`.
- It also allows renaming a file and copying the same file to separate destination folders in case you would like to have different views of the same underlying data through force-duplication.
- The `docs-manifest.txt` file should be created at the root of your project's repository.
- To explicitly specify a file/subfolder that shouldn't get copied while you are copying entire folder, you can add the source path with `!` in prefix.

An example of a `docs-manifest.txt` file is added below:
```txt
# Mappings
README.md-->folder1/folder3/hello.md
README.md-->folder2/README.md
fol1/read.md-->folder2/read.md
fol2/-->fol2/

# Don't copy these paths
!fol2/photo.jpg
!fol2/anotherfolder/
```
Notes:
1. (! Important) RHS of `-->` has to be unique across all manifest files.
2. The last line in the sample above (`fol2/-->fol2/`) shows how a folder can be copied as-is to the destination repo


## Source pipeline flow
- Job `copy-to-central-git` will run 
    - automatically for any commits on main branch of `source repo`.   
    - manually for any merge requests created where target branch is `main`.
- Performs these checks in order
    - Check if source mapping path exist 
    - Check if any source path mapping is a folder mapping and create new unique file mappings recursively
    - Check if manifest file mentions any files/folder which should not get copied and update mappings accordingly
    - Check if any mappings have spaces in filenames
    - Check if filesize for any mapping is larger than 500KB
- If any check fails, the python script exits with an error message and pipeline fails.
- If all checks pass, the python script outputs mappings which are then used to copy files to `central`.  
        