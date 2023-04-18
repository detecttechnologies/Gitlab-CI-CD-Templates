---
status: implemented
title: ADR-0002: Separate Backend, Frontend, and Master Templates for MSA and Monolithic Architectures
description: Decision to create separate backend, frontend, and master templates for MSA and Monolithic architectures, instead of keeping the files in the individual repositories
tags: adr
---

# Context and Problem Statement

We need to support both Microservices Architecture (MSA) and Monolithic Architecture. The CI/CD pipeline should be able to accommodate the specific requirements of each component and architecture type while keeping the process consistent and manageable.

# Considered Options

* Option 1: Store the CI/CD templates in the individual repositories for each project
* Option 2: Create separate backend, frontend, and master templates for MSA and Monolithic architectures, stored in a centralized location

# Decision Outcome and Reason

* Chosen option: Option 2 - Create separate backend, frontend, and master templates for MSA and Monolithic architectures, stored in a centralized location
* Reason over other options: 
    - By creating separate templates for backend and frontend components, as well as a master template, for MSA and Monolithic architectures and storing them in a centralized location, it is easier to maintain consistency and manage changes across all projects. This approach also allows for better maintainability and extensibility of the CI/CD pipeline. 
    - The master template includes the stages, rules, and triggers for the CI/CD pipeline and ensures uniformity across all projects. 
    - **Furthermore, the same templates can be used for other projects like Tpulse in the future, improving maintainability and scalability across projects.**
