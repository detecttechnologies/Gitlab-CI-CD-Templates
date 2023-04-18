---
status: implemented
title: ADR-0005: Master Pipeline Configuration and Triggers
description: Decision to use a master pipeline configuration with different triggers to manage the CI/CD process for various deployment environments in project
tags: adr
---

# Context and Problem Statement

The project has multiple deployment environments, such as development, QA, staging, and clients. In order to maintain a streamlined and efficient CI/CD process across these environments, we need to decide on a pipeline configuration that allows for easy management and triggering of pipelines specific to each environment.

# Considered Options

* Option 1: Separate pipeline configurations for each deployment environment
  * Pros:
    * Specific configurations tailored to each environment
    * Easier to isolate and fix issues related to a specific environment's pipeline setup
  * Cons:
    * Increases complexity and management overhead
    * More time-consuming to set up and maintain
* Option 2: Master pipeline configuration with different triggers for each deployment environment
  * Pros:
    * Simplifies the pipeline setup process
    * Reduces the time and effort needed for pipeline configuration and maintenance
    * Ensures consistency across all deployment environments
    * Allows for centralized control and management
    * Easy to trigger pipelines specific to each environment
  * Cons:
    * May require additional work to ensure compatibility with all deployment environments

# Decision Outcome and Reason

* Chosen option: Option 2 - Master pipeline configuration with different triggers for each deployment environment
* Reason over other options: 
  - Although ensuring compatibility between all deployment environments may require some additional work, Option 2 offers better manageability and efficiency. Using a master pipeline configuration simplifies the setup process, reduces the time and effort needed for pipeline configuration and maintenance, and ensures consistency across all deployment environments. 
  - Additionally, this method allows for better resource utilization and reduces the chances of inconsistencies and errors that may occur with separate pipeline setups. Centralized control and management, along with easy triggering of pipelines specific to each environment, further streamlines the process.
