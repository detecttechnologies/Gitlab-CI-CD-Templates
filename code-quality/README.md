# Add this pipeline to your repo

>You can just simply use the below code and paste it in your `.gitlab-ci.yml` file of your repo. Generally, this will be added to your repo by default.   

```yaml
    stages:
        - code-quality
        - test

    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/code-quality/python/.gitlab-ci.yml'
        - template: Security/SAST.gitlab-ci.yml
        - template: Security/Secret-Detection.gitlab-ci.yml

    # Gitlab SAST variables
    variables:
        SAST_EXCLUDED_ANALYZERS: "brakeman,eslint,flawfinder,gosec,kubesec,mobsf,nodejs-scan,phpcs-security-audit,pmd-apex,security-code-scan,semgrep,sobelow,spotbugs"
        SECURE_LOG_LEVEL: "info"
```