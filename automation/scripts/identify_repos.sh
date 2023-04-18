!#/bin/bash

# Set your GitLab API token and project ID as environment variables
# export CI_JOB_TOKEN=<your_personal_access_token>
# export CI_PROJECT_ID=<your_project_id>

# check if ENVIROMENT variable is set
if [ -z "$ENVIRONMENT" ]; then
    # exit with error no deploy environment found
    echo "Skipping check as no environment is specified."
    exit 0
fi

# Pass the target environment as an argument to the script
TARGET_ENVIRONMENT=$ENVIRONMENT

LATEST_TAG=$(git describe --abbrev=0 --tags)
echo "Latest tag: ${LATEST_TAG}"

PIPELINE_ID=$(curl --silent --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/pipelines?ref=main" | jq '.[] | select(.status == "success") | .id' | head -1)

DEPLOYED_TAG=$(curl --silent --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/pipelines/${PIPELINE_ID}/jobs" | jq -r --arg env "${TARGET_ENVIRONMENT}" '.[] | select(.name == "deploy" and .environment.name == $env) | .ref')

echo "Deployed tag in ${TARGET_ENVIRONMENT}: ${DEPLOYED_TAG}"

if [ "$LAST_TAG" == "$DEPLOYED_TAG" ]; then
    echo "Latest tag is already deployed in ${TARGET_ENVIRONMENT} environment in an earlier pipeline"
    exit 0
else
    echo "Latest tag is not yet deployed in ${TARGET_ENVIRONMENT} environment in an earlier pipeline"
    exit 1
fi