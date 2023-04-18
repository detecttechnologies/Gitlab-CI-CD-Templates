---
status: implemented
title: ADR-0004: Creating a Single Environment for All Clients
description: Decision to create a single environment for all clients in the CI/CD pipeline and deploy updates simultaneously for better efficiency
tags: adr
---

# Context and Problem Statement

The project has multiple clients, each requiring deployments of updates and new features. Managing separate environments and deployment processes for each client can become complex and time-consuming. We need an efficient and manageable way to deploy updates to all clients while maintaining stability and reducing potential errors.

# Considered Options

* Option 1: Creating separate environments for each client and deploying updates individually
  * Pros:
    * Allows for selective deployment to specific clients
    * Easier to isolate and fix issues related to a single client's deployment
  * Cons:
    * Requires separate deployment configuration files for each client
    * Increases complexity and management overhead
* Option 2: Creating a single environment for all clients and deploying updates simultaneously
  * Pros:
    * Simplifies the deployment process, making it easier to manage
    * Reduces the time and effort needed for deployments
    * Ensures consistency across client deployments
    * Better resource utilization
  * Cons:
    * Deployment configuration file can become long and harder to manage

# Decision Outcome and Reason

* Chosen option: Option 2 - Creating a single environment for all clients and deploying updates simultaneously
* Reason over other options: 
  - Despite the drawbacks of a longer deployment configuration file and the inability to deploy updates selectively, Option 2 offers better manageability and efficiency.
  - Creating a single environment for all clients simplifies the deployment process, reduces the time and effort needed for deployments, and ensures consistency across client deployments. 
  - Specific client deployments can be controlled by modifying the client configuration to only include a particular subset of clients.
  - Additionally, this method allows for better resource utilization and reduces the chances of inconsistencies and errors that may occur with separate environments and deployment processes.
