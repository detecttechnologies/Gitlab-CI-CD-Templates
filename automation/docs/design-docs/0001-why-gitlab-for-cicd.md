---
status: implemented
title: ADR-0001: Using GitLab CI/CD
description: Decision to use GitLab CI/CD for the pipeline
tags: adr
---

# Context and Problem Statement

We needed to choose a platform for building a CI/CD pipeline. The platform should provide the necessary features, support, and flexibility to manage our application's deployment process. It is essential to consider our existing infrastructure, team's familiarity, and the available features in the chosen platform.

# Considered Options

* GitLab CI/CD
* Jenkins

# Decision Outcome and Reason

* Chosen option: GitLab CI/CD
* Reason over other options:

  1. Our repositories are already hosted on GitLab, and we have a premium account that provides advanced CI/CD features.
  2. The team has prior experience building CI/CD pipelines using GitLab, making it a more comfortable and familiar choice.
  3. GitLab CI/CD provides built-in SAST and other templates that we can leverage for our pipeline.
  4. GitLab CI/CD supports a variety of pipeline configurations and integrations, which makes it a suitable choice for our MSA and Monolithic Architectures.

By choosing GitLab CI/CD , we benefit from the seamless integration with our existing GitLab repositories and workflow, access to advanced features and templates, a familiar platform for the team, and the ability to create and manage pipelines for our application's MSA and Monolithic Architectures. The potential limitations include platform-specific constraints or limitations and the need to reconfigure or rebuild our CI/CD pipeline if we ever decide to migrate our repositories to another platform.
