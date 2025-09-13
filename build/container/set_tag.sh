#!/bin/bash
set -e

# Set Docker IMAGE_NAME
if [ -z "$APP_NAME" ]; then
    IMAGE_NAME="${CI_REGISTRY_IMAGE}"
else
    IMAGE_NAME="${CI_REGISTRY_IMAGE}/${APP_NAME}"
fi

# Set VERSION
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
fi

# Validate VERSION doesn't contain colons (invalid for Docker tags)
if [[ "$VERSION" == *":"* ]]; then
    echo "Error: VERSION '$VERSION' contains colon character, which is invalid for Docker tags"
    echo "Docker tags cannot contain colons. Consider using semantic versioning. Else replace it with a hyphen or underscore."
    exit 1
fi

# Set IMAGE_TAG
IMAGE_TAG="${IMAGE_NAME}:${VERSION}"
echo "IMAGE_TAG=${IMAGE_TAG}" > image_tag.env
echo "IMAGE_TAG is set to: $IMAGE_TAG"