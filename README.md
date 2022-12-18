# Gitlab-CI-CD-Templates
>This repo contains different gitlab CI-CD templates that can be used to customize pipelines. You can use one or more templates and combine them in a single `.gitlab-ci.yml` file to use in your repo.

## Types of CI-CD Templates

### 1. Code Quality Checker

To include `code-quality` jobs, See [README for code-quality](code-quality/README.md).

### 2. Python Compiler

To include `python-comiler` jobs, See [README for compile/python](compile/README.md).

### 3. Knowledge Portal Connector

There are two `.gitlab-ci.yml` files which serve as source and central pipelines. `central pipeline` is already setup and all you have to do is to setup the `source pipeline` in your existing `.gitlab-ci.yml` file.

- To include `source-pipeline` jobs, See [README for knowledge-portal/source](compile/README.md).


