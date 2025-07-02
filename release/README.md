# GitLab CI/CD Release Job

A GitLab CI/CD pipeline for creating and uploading versioned **zip packages** to GitLab's [generic package registry](https://docs.gitlab.com/ee/user/packages/generic_packages/).

---

## What does it do?

When you push to:

- **A Git tag** → publishes with that tag as the version
- **`main` branch** → publishes with `production` as the version
- **`develop` branch** → publishes with `dev` as the version

The job will:

1. Install dependencies (zip, curl, jq)  
2. Zip your specified files and folders into `release.zip`  
3. Delete any existing package with the same version  
4. Upload the new `release.zip` to the GitLab Package Registry

---

## How to configure

The `release` job in `.gitlab-ci.yml` supports a **RELEASE_FILES** variable that defines which files and folders to include in the release.

You can define this variable in:

- The `.gitlab-ci.yml` itself (default value)
- The GitLab UI when triggering a pipeline manually
- GitLab project or group-level variables

Add in `.gitlab-ci.yml`:

```yaml
include:
    - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/release/.gitlab-ci.yml'

variables:
  RELEASE_FILES: "refresh_setup.sh,setup"
