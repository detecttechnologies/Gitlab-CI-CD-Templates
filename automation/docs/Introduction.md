# Introduction to automation CI/CD pipeline

The project aims to automate the build, test, and deploy aspect for both MSA and Monolith architectures. This guide is aimed at introducing the design, working, and limitations of CI/CD pipeline.

[TOC]

## Design

There are separate CI/CD templates for backend and frontend repositories which contain pipeline configurations for running the jobs. These templates are stored in a central/master repository and included in the required BE or FE repo. The reason for keeping them in a central location is that the templates are designed to be reusable and allow us to control the pipeline without making any change in a specific BE or FE repo.  

### Pre-requisites

In order to add the pipeline template to any specific repo, refer [Usage Guide](Usage.md). However, before the pipeline can function, there are some requirements that needs to be satisfied.

1. **MSA backend**

    - Infrastructure related things like, ECR repo, ECS Cluster, Task definition, and ECS service has to be present. 
    - The pipeline reads the existing task definition, modifies the image tag in container definition, and updates the ECS service.
    - Any database related setup(migration, adding data) has to be done manually.

2. **MSA frontend**

    - Infrastructure related things like, EC2 VM needs to be setup with ssh keys available. 
    - Root frontend app and `dist` folder has to be setup initially.
    - The pipeline builds the dist and uploads its contents to destination dist folder in VM.

### Deployment environments

Environments describe where code is deployed. Each time GitLab CI/CD deploys a version of code to an environment, a deployment is created. [Learn More](https://docs.gitlab.com/ee/ci/environments/).

Each time we are deploying our code for an FE or BE repo, we add an `environment` keyword in the job which tells it the name of the environment. A sample job would look like :

```yml
deploy:
    stage: deploy
    environment:
        name: dev
    script:
        - echo "run deploy job"
```
This will create a `dev` environment, which can be accessed from `Deployments`-->`Environments`-->`<environment_name>`.

> Having an environment also allow to rollback any deployment through the UI itself, where it runs the `deploy` job for any previous commit.

### Authentication

- We require these four credentials if we want to use AWS ECR or ECS
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_ACCOUNT_ID
    - AWS_DEFAULT_REGION

- We require these 2 credentials if we want to use AWS EC2
    - EC2_IP_ADDRESS
    - SSH_PRIVATE_KEY 

> These credentials are to be stored in a `.toml` config file for each environment. Refer to [Usage Guide](Usage.md) for more details.

## Pipeline lifecycle

1. **MR is created with target branch `develop` on any individual repo.**

    - Jobs in build and test stages will run on `merge_requests` in order to verify
        - the change hasn't broken `docker build` or `npm run build` process.
        - the change passes all existing tests available to the MR.

2. **MR is accepted and changed are merged with target branch `develop`.**

    - Jobs in build and deploy stages will run
        - In BE repo, the docker image is built and tagged with **dev** tag in `build` stage. The image is then pushed to ECR and deployed to ECS with service updated with latest task definition in `deploy` stage.
        - In FE repo, dist folder is created in `build` stage and its content are uploaded to EC2 in `deploy` stage.
    - For `dev` environment, we are using **Continuous Deployment**, and hence the jobs will deploy the latest code without any manual intervention. There are situations where pipeline will break the deployment, knowing about these will help troubleshoot/fix such issues. Refer to [Troubleshoot](../docs/Troubleshooting.md).
    - You can also use master repo to trigger the pipeline for `develop` branch if need be. 
    - Go to master repo. **CI/CD-->RUN PIPELINE**. Select DEPLOYMENT_ENVIRONMENT as `dev`, CLIENTS as `none`, and trigger the pipeline.  

3. **MR is created with target branch `test` on any individual repo.**

    - Jobs in build and test stages will run on `merge_requests` in order to verify
        - the change hasn't broken `docker build` or `npm run build` process.
        - the change passes all existing tests available to the MR. 

4. **MR is accepted and changed are merged with target branch `test`.**
    - Jobs in build and deploy stages will run
        - In BE repo, the docker image is built and tagged with **qa** tag in `build` stage. The image is then pushed to ECR and deployed to ECS with service updated with latest task definition in `deploy` stage.
        - In FE repo, dist folder is created in `build` stage and its content are uploaded to EC2 in `deploy` stage.
    - Jobs in build and deploy stages will run. The deploy stage will be a manual stage if the pipeline is triggered by code commit on the repo.
    - Pipeline on `test` can also be controlled using the master repo. In this scenario, the deployment will be an automatic process.   
    - Go to master repo. **CI/CD-->RUN PIPELINE**. Select DEPLOYMENT_ENVIRONMENT as `qa`, CLIENTS as `none`, and trigger the pipeline.     

5. **MR is created with target branch `main` on any individual repo.**

    - Jobs in build and test stages will run on `merge_requests` in order to verify
        - the change hasn't broken `docker build` or `npm run build` process.
        - the change passes all existing tests available to the MR. 

6. **MR is accepted and changed are merged with target branch `main`.**

    - Jobs in build and deploy stages will run
        - In BE repo, the docker image is built and tagged with **latest version** tag in `build` stage. The image is then pushed to ECR and deployed to ECS with service updated with latest task definition in `deploy` stage.
        - In FE repo, dist folder is created in `build` stage and its content are uploaded to EC2 in `deploy` stage.
    - Jobs in build and deploy stages will run. The deploy stage will be a manual stage if the pipeline is triggered by code commit on the repo.
    - Pipeline on `main` can also be controlled using the master repo. In this scenario, the deployment will be an automatic process.   
    - If you want to trigger for `staging` environment
        - Go to master repo. **CI/CD-->RUN PIPELINE**. Select DEPLOYMENT_ENVIRONMENT as `staging`,  CLIENTS as `none`, and trigger the pipeline. 

7. **Clients deployment.**

    - Client deployments can only be triggered through the master repo.
    - Jobs in build and deploy stages will run on `main` branch.
        - In BE repo, the docker image is built and tagged with **version** tag in `build` stage. The image is then pushed to ECR and deployed to particular client ECS cluster with service updated with latest task definition in `deploy` stage.
        - In FE repo, dist folder is created in `build` stage and its content are uploaded to client's EC2 in `deploy` stage.
    - Go to master repo. **CI/CD-->RUN PIPELINE**. Select DEPLOYMENT_ENVIRONMENT as `clients`, CLIENTS as `all` or a `<comma separated client names>` and trigger the pipeline. 
