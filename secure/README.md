# Security Scanning Pipeline

This module provides GitLab CI templates to run application security scans and produce human‑readable reports. It includes:

- SAST (Semgrep) scanning
- Secret Detection
- Optional Container Scanning of your built image (See [bulid job](../build/README.md) to setup build job) 
- A report aggregation job that generates PDF reports and a `metrics.txt` for showing scan reports in Gitlab MR widget

## Quick Start

Add the following to your project's `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - report

include:
  # Core security scans and report generation
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/secure/.gitlab-ci.yml'
  # Optional: Container Scanning (requires the build job)
  - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/secure/container-scanning.gitlab-ci.yml'

variables:
  CONTAINER_SCAN_DISABLED: "false" # only needed if changing to 'true'

  
```

**For building and publishing the image used by Container Scanning, refer to the build module documentation: see [README for build/container](../build/README.md).**

## What You Get

- `semgrep-sast` (from GitLab template)
  - Produces: `gl-sast-report.json`
- `secret_detection` (from GitLab template)
  - Produces: `gl-secret-detection-report.json`
- `container_scanning` (optional; via Jobs/Container-Scanning template)
  - Produces: `gl-container-scanning-report.json`
- `analyze_reports` (from this module)
  - Produces artifacts:
    - `sast-report.pdf`
    - `secret-detection-report.pdf`
    - `container-scanning-report.pdf` (if scan was enabled and ran)
    - `metrics.txt` (GitLab metrics report; counts of findings to be shown in MR widget)

## When It Runs

By default, the jobs are configured to run on:
- Git tags
- Merge Request pipelines
- Commits to the `main` branch

You can adjust this behavior by overriding `rules:` in your project.

## Variables
- `CONTAINER_SCAN_DISABLED` (default: `false`)
  - Set to `"true"` to disable the container scanning job.

## Troubleshooting

- Missing `gl-*.json` files:
  - Ensure the corresponding scan job ran and produced artifacts.
  - Check `rules:` filters in your pipeline.
- Empty PDFs:
  - Indicates zero findings or missing JSON. Verify upstream jobs and artifacts.
- Container scanning not producing a report:
  - Confirm an image exists at `$CI_REGISTRY_IMAGE:$VERSION` for the current pipeline context (tag/merge/latest).
