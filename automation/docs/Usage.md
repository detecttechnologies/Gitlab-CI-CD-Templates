# Automation CI/CD Pipeline - Usage Guide

This document provides a comprehensive explanation on how to setup the CI/CD pipelines for both Microservices Architecture (MSA) and Monolithic Architecture projects.

[TOC]

## Microservices Architecture (MSA)

In the MSA approach, applications are broken down into smaller, independently deployable services. The CI/CD pipeline configuration for MSA projects is split between backend and frontend repositories.

### Backend Repository Configuration

1. Navigate to your backend repository, which contains your Django application code.
2. Create a `.gitlab-ci.yml` file in the root of your repository, which will define your pipeline configuration.
3. Use the `include` keyword in the `.gitlab-ci.yml` file to reference a template that handles build, test, and deploy jobs for your Django application.

```
include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/pipelines/backend.gitlab-ci.yml'

variables:
  GIT_STRATEGY: clone

```
**Setup CI/CD variables for credentials and deployment related configurations and scripts**

- Add `.toml` configuration file variables in your CI/CD variables
  - Navigate to `Settings-->CI/CD-->Variables`
  - Add 3 variables, one for each internal environment: dev, test, and qa. Variable names are:
    1. dev_DEPLOYMENT_CONFIG 
    2. qa_DEPLOYMENT_CONFIG
    3. staging_DEPLOYMENT_CONFIG
  - These 3 variables are essentially configuration files which contain environment specific aws and ec2 credentials along with repos information
  - To create this file, refer this sample [sample toml config](../configs/sample.toml)

### Frontend Repository Configuration

1. Navigate to your frontend repository, which contains your Angular application code.
2. Create a `.gitlab-ci.yml` file in the root of your repository, which will define your pipeline configuration.
3. Use the `include` keyword in the `.gitlab-ci.yml` file to reference a template that handles build, test, and deploy jobs for your Angular application. 

```
include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/pipelines/frontend.gitlab-ci.yml'

variables:
  GIT_STRATEGY: clone

```
**Setup CI/CD variables for credentials and deployment related configurations and scripts**

- Add `.toml` configuration file variables in your CI/CD variables
  - Navigate to `Settings-->CI/CD-->Variables`
  - Add 3 variables, one for each internal environment: dev, test, and qa. Variable names are:
    1. dev_DEPLOYMENT_CONFIG 
    2. qa_DEPLOYMENT_CONFIG
    3. staging_DEPLOYMENT_CONFIG
  - These 3 variables are essentially configuration files which contain environment specific aws and ec2 credentials along with repos information
  - To create this file, refer this sample [sample toml config](../configs/sample.toml)
- To connect to VPN for EC2 deployments, add a config file that contains VPN configuraion in your FE repo. Refer to [sample vpn config](../configs/vpn_config_sample.toml). 


### Master Repository Configuration

1. Navigate to your master repository,or create one.
2. Create a `.gitlab-ci.yml` file in the root of your repository, which will define your pipeline configuration.

```
include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/pipelines/master.gitlab-ci.yml'

variables:
  GIT_STRATEGY: clone

```

### Automation Testing Repository Configuration

1. Navigate to your automation testing repository.
2. Create a `.gitlab-ci.yml` file in the root of your repository, on the branch you want to run the tests, which will define your pipeline configuration.

```
include:
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/pipelines/qa_test.gitlab-ci.yml'

variables:
  GIT_STRATEGY: clone

```

**Setup CI/CD variables for credentials and deployment related configurations and scripts**

- Add `.toml` configuration file variables in your CI/CD variables
  - Navigate to `Settings-->CI/CD-->Variables`
  - Add 3 variables, one for each internal environment: dev, test, and qa. Variable names are:
    1. dev_DEPLOYMENT_CONFIG 
    2. qa_DEPLOYMENT_CONFIG
    3. staging_DEPLOYMENT_CONFIG
  - These 3 variables are essentially configuration files which contain environment specific aws and ec2 credentials along with repos information
  - To create this file, refer this sample [sample toml config](../configs/sample.toml)

- Apart from the default 3 configs, you can also add `n` no. of client configs. Keep the name of the variable in format: `<client_name>_DEPLOYMENT_CONFIG`.

- Since we are also using `all` keyword for simultaneous clients deployment, we have to add `ALL_CLIENTS` variable which would be comma separated client names.
- FInally add `PREFIX_PATH` which contains the common prefix path for all repos.



### Triggering the pipeline

1. Navigate to your master repository, which contains all the CI/CD templates related to the pipeline.
2. Go to CI/CD, `RUN PIPELINE` and select the environment for which you want to run the pipeline for.
3. Before clicking on run, there are 2 pipeline variables to choose from
  - DEPLOY_ENVIRONMENT: select from dev, qa, staging, clients.
  - CLIENTS: By default, it is set to **'none'**. Leave it be if you chose, dev, qa, or staging. You can set it to **'all'**, if you want to simultaneously deploy for all clients. Or, you can give a list of client names separated by commas(no spaces).   


## Monolithic Architecture

In Monolithic Architecture, applications are built as a single, unified unit. The CI/CD pipeline configuration for monolithic projects is similar to that of MSA projects, with the primary difference being that there is only one backend repository and one frontend repository.

To configure the CI/CD pipelines for a Monolithic Architecture project, follow the steps outlined in the MSA section above, applying them to the single backend and frontend repositories in your monolithic application.

**WIP**
