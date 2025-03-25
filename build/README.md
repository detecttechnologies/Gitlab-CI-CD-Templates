# CI/CD Pipeline Components

This README provides documentation for two GitLab CI components: a Docker image build pipeline and a Node.js package build pipeline. Both are designed to automate the build and publication process triggered by tags and merge requests.

## Overview

These pipelines offer:
- Automated builds triggered by Git tags and merge requests
- Consistent versioning based on Git tags
- Multi-platform Docker image support via BuildX
- Node.js package building with version management

## Getting Started

### Prerequisites

To use these pipelines, you'll need:
- A GitLab repository with CI/CD enabled
- Docker or Node.js project structure (Dockerfile or package.json)
- Appropriate GitLab runner tags configured

### When It Runs

- When a Git tag is created: builds images tagged with both the Git tag and `latest`
- When a merge request is opened/updated: builds images tagged with `merge`

## Docker Image Build Pipeline

The Docker build pipeline automatically builds and publishes Docker images to GitLab Container Registry using your Dockerfile.

### Adding the pipeline

To include the build pipeline in your project, create/update a `.gitlab-ci.yml` file in your repository root with the following content:

```yaml
include:
    - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/build/docker/.gitlab-ci.yml'

variables:
    DOCKERFILE_PATH: "Dockerfile"
    PLATFORMS: "linux/amd64"
    APP_NAME: "deploy"
```

### Explanation of Variables

| Variable         | Description                                                                 | Default Value   | Optional |
|-----------------|-----------------------------------------------------------------------------|---------------|----------|
| **DOCKERFILE_PATH** | Specifies the location of the Dockerfile used for building the image. | `Dockerfile`  | No       |
| **PLATFORMS**    | Defines the target platform(s) separated by commas for the Docker image build. Supported values include `linux/amd64`, `linux/arm64`, `linux/arm/v7`, `linux/ppc64le`, `linux/s390x`. | `linux/amd64` | Yes      |
| **APP_NAME**     | Sets the name of the application, which can be used for tagging the image or organizing builds within the pipeline. | `deploy`      | Yes      |
| **BUILD_ARGS**   | Allows passing build arguments to the Docker build process. Arguments should be provided as a comma-separated list (e.g., `ARG1=value1,ARG2=value2`). | N/A           | Yes      |


## Node.js Package Build Pipeline

The Node.js build pipeline automatically builds and publishes Node.js packages to Gitlab Package Registry based on your package.json file.

#### Adding the pipeline

To include the build pipeline in your project, create/update a `.gitlab-ci.yml` file in your repository root with the following content:

```yaml
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/build/node/.gitlab-ci.yml'
```

## Troubleshooting

- Ensure your Dockerfile or package.json exists in the repository
- Check that the runner tags (`amd64`, `saas-linux-medium-amd64`) are available in your GitLab instance
- Verify you have the correct permissions to push to the registry

## Support

For issues or improvements, please contact Platform team.