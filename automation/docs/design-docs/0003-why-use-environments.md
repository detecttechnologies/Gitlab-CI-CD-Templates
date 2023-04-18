---
status: implemented
title: ADR-0003: Using GitLab Environments for Deployment inCI/CD Pipeline
description: Decision to use GitLab Environments for managing deployment environments and configurations in the CI/CD pipeline for better control, traceability, and rollback capabilities
tags: adr
---

# Context and Problem Statement

The project requires deployments to multiple environments, such as development, QA, staging, and client environments. Managing the deployment configurations and environment-specific settings in the CI/CD pipeline is crucial for seamless and efficient deployment across different environments. 

# Considered Options

* Option 1: Not using GitLab Environments for deployment management
* Option 2: Using GitLab Environments for deployment management

# Decision Outcome and Reason

* Chosen option: Option 2 - Using GitLab Environments for deployment management
* Reason over other options: 
    - Using GitLab Environments provides better control and traceability of the deployments in the CI/CD pipeline. 
    - GitLab Environments allow for easier management of deployment configurations and environment-specific settings, providing a clear overview of which code is deployed in each environment. 
    - Additionally, GitLab Environments support rollback capabilities, enabling the ability to revert to the last successful deployment in case of failures, ensuring stability and reducing the risk of errors. 
