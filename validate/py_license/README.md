# GitLab CI/CD Configuration

This GitLab CI/CD pipeline checks for python package licenses based on an approved list.

## Usage

To include this configuration in your GitLab project, add the following to `.gitlab-ci.yml`:

```yaml
    stages:
        - test
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/validate/py_license/.gitlab-ci.yml'
    
    license_checker:
        image: <docker image where packages are installed>
```

Modify as needed for your project’s requirements.