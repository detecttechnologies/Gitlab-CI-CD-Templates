# Python Compile Pipeline

Using Cython, Python files can be compiled for distribution across various versions of Python and CPU architectures. However, it's important to note that the compilation is not static, and therefore, any dependencies from PyPI will still need to be installed separately.

To utilize the CI/CD template, it's necessary to add it to your project's `.gitlab-ci.yml` file and set up certain configurations such as pipeline settings and CI/CD variables.

## Usage (Configuring Pipeline)

### Adding CI/CD Variable
    
To set up CI/CD variables, navigate to Settings > CI/CD > Variables in your GitLab project and follow these steps:
1. Set the `BUILD_OUTPUT_REPO` variable to the path of the destination repository where you want to push the built artifacts. 
    - path is a substring of repo url and should be of the form `<org-name>/../../<YOUR_SOURCE_REPO>.git`
2. Keep the variable `protected` to ensure that the job can access the variable only from a protected branch.


### Sample configuration 

```yml
stages:
  - build
  - push

include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/compile/python/.gitlab-ci.yml'

variables:
    COPY_FILES: |
        ./Dockerfile
        ./docker-compose.yml
        ./USAGE.md
        ./TEST.md
        ./README.md
    GIT_STRATEGY: clone #REQUIRED
    GIT_DEPTH: 1  
    EXCLUDE_FILES: |
        ./folder1/test.py
        ./folder2

# Add this if you only want to build for specific versions
# IN following case, we are building (py3.6,py3.7) for amd64(x86_64) and (py3.6, py3.7) for arm64(aarch64) architectures respectively
build_binaries:
    parallel:
        matrix:
            - TAG: amd64
              PLATFORM: amd64
              VERSION: [py3.6,py3.7]
            - TAG: armv8
              PLATFORM: arm64
              VERSION: [py3.6,py3.7] 
```

### Choosing version and architecture 
By default, the pipeline tries to build all combinations of Python versions and CPU architectures. However, you can modify this behavior to build specific versions by adding the following snippet to the `.gitlab-ci.yml` file of the source repository and modify the `matrix`.

```yaml
build_binaries:
    parallel:
        matrix:
            - TAG: amd64
              PLATFORM: amd64
              VERSION: [py3.5,py3.6,py3.7,py3.8,py3.9,py3.10]
            - TAG: armv8
              PLATFORM: arm64
              VERSION: [py3.5,py3.6,py3.7,py3.8,py3.9,py3.10] 
            - TAG: armv8
              PLATFORM: armv7
              VERSION: [py3.5,py3.6,py3.7,py3.8,py3.9,py3.10]
```
In the above snippet, `TAG` refers to the GitLab runner being used to run the job, `PLATFORM` refers to the CPU architecture, and `VERSION` refers to the Python version.

### Pipeline Variables

To configure the pipeline, you can use the following variables:

- `GIT_STRATEGY: clone` is **required** to ensure that the pipeline in source repository doesn't contain cached files.
- `GIT_DEPTH: 1` can be set accordingly. By default it is set to 20 by gitlab.
- `GIT_SUBMODULE_DEPTH: 1` can be set accordingly
- `COPY_FILES`: Use this as gitlab multiline variable and provide full path of files/folders that needs to be copied to destination. No `.py` or `.so` files will be copied using this variable. It will skip such files, even if you give entire folder to copy.
- `EXCLUDE_FILES`: Use this as gitlab multiline variable and provide full path for files or folders that should be excluded from cythonization. 
- `RUN_SCRIPTS`: Use this as gitlab multiline variable if you want to run any script in the pipeline before copying over the files to destination.

