#!/bin/bash

# Initialize FAIL variable
FAIL=0

# Check Semgrep SAST Report
if [ -f semgrep-sast-report.json ]; then
    if jq -e '.vulnerabilities[]' semgrep-sast-report.json; then
        echo "Vulnerabilities detected in Semgrep report!"
        FAIL=1
    else
        echo "No vulnerabilities found in Semgrep report."
    fi
else
    echo "Semgrep report not found."
fi

# Check Node.js Scan SAST Report
if [ -f nodejs-scan-sast-report.json ]; then
    if jq -e '.vulnerabilities[]' nodejs-scan-sast-report.json; then
        echo "Vulnerabilities detected in Node.js scan report!"
        FAIL=1
    else
        echo "No vulnerabilities found in Node.js scan report."
    fi
else
    echo "Node.js scan report not found."
fi

# Check Secret Detection Report
if [ -f secret-detection-report.json ]; then
    if jq -e '.vulnerabilities[]' secret-detection-report.json; then
        echo "Secrets detected!"
        FAIL=1
    else
        echo "No secrets found."
    fi
else
    echo "Secret detection report not found."
fi

# Fail the Pipeline if Any Issues are Detected
if [ "$FAIL" -eq "1" ]; then
    echo "Failing the pipeline due to detected issues."
    exit 1
fi
