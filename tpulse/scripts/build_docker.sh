#!/bin/bash

# Remove the worktree using git worktree remove if exits
git worktree remove ../temp-worktree || true

# Check if DEPLOY_ENVIRONMENT variable is set
if [ -z "$DEPLOY_ENVIRONMENT" ]; then
    # Build Docker image with merge request tag
    TAG="merge_request"
    git worktree add ../temp-worktree
else
    # Determine the image tag based on DEPLOY_ENVIRONMENT value
    if [ "$DEPLOY_ENVIRONMENT" = "clients" ] || [ "$DEPLOY_ENVIRONMENT" = "staging" ]; then
        export TAG=$(git describe --abbrev=0 --tags)
        git worktree add ../temp-worktree $TAG
    
    elif [ "$DEPLOY_ENVIRONMENT" = "dev" ] || [ "$DEPLOY_ENVIRONMENT" = "qa" ]; then
        TAG=$DEPLOY_ENVIRONMENT
        git worktree add ../temp-worktree
    
    else
        echo "Unrecognized DEPLOY_ENVIRONMENT value: $DEPLOY_ENVIRONMENT"
        exit 1
    fi
fi

# cd into the worktree
cd ../temp-worktree
cat ../.gitlab-ci.yml

# Log in to the container registry
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

# Build and tag the Docker image
docker build -t $CI_REGISTRY_IMAGE:$TAG -f docker/Dockerfile .

docker push $CI_REGISTRY_IMAGE:$TAG

cd -
# Remove the worktree using git worktree remove
git worktree remove ../temp-worktree
