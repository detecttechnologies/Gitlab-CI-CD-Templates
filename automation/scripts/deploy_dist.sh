#!/bin/bash

# SSH configuration
eval $(ssh-agent -s)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

# # Remove it later
# cd $CI_PROJECT_DIR/dist
# mv -v s-and-s s-and-s-cicd 
# cd -

# Check if DEPLOY_ENVIRONMENT variable is set
if [ -z "$DEPLOY_ENVIRONMENT" ]; then
    # exit with error no deploy environment found
    echo "No deploy environment found."
    exit 1
else
    python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/scripts/deploy_ec2.py)" "$DEPLOY_CONFIG"
fi
