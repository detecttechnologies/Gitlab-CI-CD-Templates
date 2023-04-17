---
status: implemented
title: ADR-0006: Refactor Pipeline Scripts to Py and Sh Templates
description: Decision to refactor logic from pipeline scripts to py and sh templates for better code maintenance and reusability.
tags: adr
supersedes: ADR-0002
---

# Context and Problem Statement

In the previous ADR-0002, we decided to create separate backend, frontend, and master templates for MSA and Monolithic architectures. As the project evolves, there is a need to improve code maintainability and reusability. Refactoring logic from pipeline scripts to py and sh templates can help achieve these goals.

# Considered Options

* Option 1: Keep the current pipeline scripts without refactoring
* Option 2: Refactor logic from pipeline scripts to py and sh templates

# Decision Outcome and Reason

* Chosen option: Option 2 - Refactor logic from pipeline scripts to py and sh templates
* Reason over other options:
    - Refactoring the logic from pipeline scripts to py and sh templates improves code maintenance and prevents the need to create similar multiple build and deploy jobs.
    - By moving the templates for pipelines and scripts to our GitHub repo, we can easily add and update code snippets, further improving maintainability.
    - This change also allows for better reusability of the templates in future projects, as we can create separate master repos for those projects and reuse the templates as needed.
