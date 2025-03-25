# GitLab CI/CD Configuration

This GitLab CI/CD pipeline ensures code quality, security, and secret detection using predefined templates and custom jobs.

## Included Templates

- **Code Quality** (`Jobs/Code-Quality.gitlab-ci.yml`)
- **Static Application Security Testing (SAST)** (`Security/SAST.gitlab-ci.yml`)
- **Secret Detection** (`Security/Secret-Detection.gitlab-ci.yml`)

## Job Descriptions

### **Semgrep SAST**
- Runs security analysis using Semgrep.
- Saves `semgrep-sast-report.json`.
- Runs on any commit branch and merge request events.

### **Node.js Scan SAST**
- Runs SAST for Node.js projects if `package.json` exists.
- Saves `nodejs-scan-sast-report.json`.
- Runs on any commit branch and merge request events.

### **Secret Detection**
- Detects hardcoded secrets.
- Saves `secret-detection-report.json`.
- Runs on any commit branch and merge request events.

### **Code Quality**
- Analyzes code quality.
- Skips if `$CODE_QUALITY_DISABLED` is set.
- Runs only on merge request events.

### **Analyze Reports**
- Aggregates test reports.
- Fetches an external report analysis script.
- Allowed to fail without affecting the pipeline.
- Runs on any commit branch and merge request events.

## Usage

To include this configuration in your GitLab project, add the following to `.gitlab-ci.yml`:

```yaml
    stages:
        - test
        - report
    include:
        - remote: 'https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/main/gl-test/.gitlab-ci.yml'
```

Modify as needed for your project’s requirements.