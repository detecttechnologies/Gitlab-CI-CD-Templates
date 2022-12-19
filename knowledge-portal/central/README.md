# Setting up pipeline in central repository

>You can just simply use the below code and paste it in your `.gitlab-ci.yml` file of your repo.

```yaml
stages:
    - merge_request_to_source
include:
    - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/knowlwdge-portal/central/.gitlab-ci.yml'
```

## Setting up Access Token in central repository

1. Go to `Settings >> Access Tokens`.
2. Set `Token name = PUSH_TOKEN`. This is important and you can't choose any other name without modifying the source pipeline as well.
3. Select the role `Maintainer` and `write_repository` as the scope of token.
4. `Create project access token` will create a unique token for you that can then be shared with people setting up the `knowledge-portal/source` pipeline.
