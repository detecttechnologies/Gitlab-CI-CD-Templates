---
status: implemented
title: ADR-0007: Creating Separate Environments for Each Client
description: Decision to revert to separate environments for each client in the CI/CD pipeline to gain finer control over deployments
tags: adr
supersedes: ADR-0004
---

# Context and Problem Statement

In ADR-0004, we decided to create a single environment for all clients and deploy updates simultaneously. However, this approach has its limitations, and we need a more fine-grained control over deployments. By creating separate environments for each client, we can have better control over deployment processes and selectively deploy updates to specific clients.

# Considered Options

* Option 1: Creating separate environments for each client and deploying updates individually
* Option 2: Continuing with a single environment for all clients and deploying updates simultaneously

# Decision Outcome and Reason

* Chosen option: Option 1 - Creating separate environments for each client and deploying updates individually
* Reason over other options:
  - While the single environment approach (Option 2) offered some benefits, it lacked the fine-grained control necessary to manage individual client deployments effectively.
  - With Option 1, we can use tokens to get the latest deployment status of a repo for any particular client and decide whether or not to run our deploy jobs more effectively.
  - Creating separate environments for each client allows for selective deployment and makes it easier to isolate and fix issues related to a single client's deployment.
  - Although this approach increases complexity and management overhead, the benefits of finer control and better visibility into individual client deployments outweigh the disadvantages.
