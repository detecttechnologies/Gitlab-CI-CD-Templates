#!/bin/bash

# Initialize variables
FAIL=0

# Check Semgrep SAST Report
if [ -f gl-sast-report.json ]; then
    semgrep_count=0
    semgrep_count=$(jq '.vulnerabilities | length' gl-sast-report.json)
    if [ "$semgrep_count" -gt 0 ]; then
        echo "Vulnerabilities detected in Semgrep report: $semgrep_count"
        FAIL=1
    else
        echo "No vulnerabilities found in Semgrep report."
    fi
else
    echo "Semgrep report not found."
fi

# Check Secret Detection Report
if [ -f gl-secret-detection-report.json ]; then
    secrets_count=0
    secrets_count=$(jq '.vulnerabilities | length' gl-secret-detection-report.json)
    if [ "$secrets_count" -gt 0 ]; then
        echo "Secrets detected: $secrets_count"
        FAIL=1
    else
        echo "No secrets found."
    fi
else
    echo "Secret detection report not found."
fi

# Check Container Scanning Report
if [ -f gl-container-scanning-report.json ]; then
    container_vuln_count=0
    container_vuln_count=$(jq '.vulnerabilities | length' gl-container-scanning-report.json)
    if [ "$container_vuln_count" -gt 0 ]; then
        echo "Container vulnerabilities detected: $container_vuln_count"
        FAIL=1
    else
        echo "No container vulnerabilities found."
    fi
else
    echo "Container scanning report not found."
fi

# Generate Metrics Report
cat <<EOF > metrics.txt
# HELP semgrep_vulnerabilities Number of vulnerabilities detected by Semgrep SAST
# TYPE semgrep_vulnerabilities gauge
semgrep_vulnerabilities $semgrep_count

# HELP secret_detection_vulnerabilities Number of secrets detected
# TYPE secret_detection_vulnerabilities gauge
secret_detection_vulnerabilities $secrets_count

# HELP container_vulnerabilities Number of vulnerabilities detected by Container Scanning
# TYPE container_vulnerabilities gauge
container_vulnerabilities $container_vuln_count
EOF

echo "Metrics report generated: metrics.txt"

export FAIL=$FAIL