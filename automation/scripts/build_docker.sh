#!/bin/bash

# Check if DEPLOY_ENVIRONMENT variable is set
if [ -z "$DEPLOY_ENVIRONMENT" ]; then
    # Build Docker image with merge request tag
    TAG="merge_requests"
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
fi

# cd into ROOT_FOLDER
cd $ROOT_FOLDER

# Log in to the container registry
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

# Build and tag the Docker image
docker build -t $CI_REGISTRY_IMAGE:$TAG -f docker/Dockerfile .

docker push $CI_REGISTRY_IMAGE:$TAG

cd -
