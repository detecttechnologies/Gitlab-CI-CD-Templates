#!/bin/bash
set -e

# Set Docker IMAGE_NAME and VERSION
if [ -z "$APP_NAME" ]; then
    IMAGE_NAME="${CI_REGISTRY_IMAGE}"
else
    IMAGE_NAME="${CI_REGISTRY_IMAGE}/${APP_NAME}"
fi

if [ -z "$VERSION" ]; then
    # Set VERSION to CI_COMMIT_TAG if available
    if [ -n "$CI_COMMIT_TAG" ]; then
        VERSION="$CI_COMMIT_TAG"
    elif [ "$CI_PIPELINE_SOURCE" == "merge_request_event" ]; then
        VERSION="merge"
    elif [ "$CI_COMMIT_BRANCH" == "main" ]; then
        VERSION="latest"
    else
        VERSION="$CI_COMMIT_BRANCH"
    fi
else  
    VERSION="$CI_COMMIT_BRANCH"
fi

IMAGE_TAG="${IMAGE_NAME}:${VERSION}"

# Create variables file for other jobs to source
printf 'export IMAGE_TAG="%s"\n' "$IMAGE_TAG" > build_variables.env

echo "IMAGE_TAG is set to: $IMAGE_TAG"