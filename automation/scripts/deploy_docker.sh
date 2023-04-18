#!/bin/bash

# Check if DEPLOY_ENVIRONMENT variable is set
if [ -z "$DEPLOY_ENVIRONMENT" ]; then
    # exit with error no deploy environment found
    echo "No deploy environment found."
    exit 1
else
    # Determine the image tag based on DEPLOY_ENVIRONMENT value
    if [ "$DEPLOY_ENVIRONMENT" = "clients" ] || [ "$DEPLOY_ENVIRONMENT" = "staging" ]; then
        export TAG=$(git describe --abbrev=0 --tags)
    
    elif [ "$DEPLOY_ENVIRONMENT" = "dev" ] || [ "$DEPLOY_ENVIRONMENT" = "qa" ]; then
        TAG=$DEPLOY_ENVIRONMENT

    else
        echo "Unrecognized DEPLOY_ENVIRONMENT value: $DEPLOY_ENVIRONMENT"
        exit 1
    fi

    python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/scripts/push_ecr.py)" "${DEPLOY_CONFIG}" $TAG

    python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/scripts/deploy_ecs.py)" "${DEPLOY_CONFIG}" $TAG
fi
