# Setting up pipeline in central repository

>You can just simply use the below code and paste it in your `.gitlab-ci.yml` file of your repo.

```yaml
stages:
    - push
include:
    - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowledge-portal/central/.gitlab-ci.yml'
```

## Setting up Access Token in central repository

1. Go to `Settings >> Access Tokens`.
2. Set `Token name = PUSH_TOKEN`. This is important and you can't choose any other name without modifying the source pipeline as well.
3. Select the role `Maintainer` and `write_repository` as the scope of token.
4. `Create project access token` will create a unique token for you that can then be shared with `maintainers` setting up individual `source` pipelines.


## Setting up BOT_ACCESS_TOKEN variable 

1. Go to `Settings >> CI/CD >> Variables`
2. Click on `Add variable`. 
3. Give the name `BOT_ACCESS_TOKEN` in `Key` field and `Value` field will be provided by your maintainers.
4. Click on `Add variable` button to confirm changes.

## Working of pipeline

### 1. If same file from `source` exists in multiple locations(duplicates) at `central`, and both files are modified simultaneously
- Let's say `duplicate1` is declared before `duplicate2` in your `docs-manifest` file
- Then `duplicate2`, which is mentioned later, will take precedence and will be pushed as truth back to `source` repo.
- After MR is accepted at `source`, the pipeline will again run and `duplicate1` will also get replaced by contents of `duplicate2`.

### 2. Files from multiple repos are modified simultaneously
- Since, RHS of `docs-manifest` is unique, we can identify the `source` repo the file belongs to from the suffix(repo_name) present in `docs-manifest_suffix.txt`.
- We then clone those repos in unique folders, commit our changes, and push to source repo.

### 3. Recognise if a commit on `central` happened through `Knowledge Portal`
- All commits from `Knowledge Portal` starts with commit message `docs:....`
- We check this substring `docs:` in the commit message to ensure the same.

    Notes: `Knowledge Portal` creates new commits for every changed file, if multiple files on `Knowledge Portal` are modified and saved at almost exact time, the pipeline on `central` repo only runs for latest commit(best guess: this only happens when you do a `Force Sync` opeartion under `Storage` on wikijs). 
    -  To resolve, this issue, we check last 5 commits starting from the latest commit until `docs:` pattern break.  
    - A drawback of this implementation is that, it will add commits to same MR incase pipeline actually ran for previous commits as well.    




