# Variables: (First 2 variables are set by the set-build-vars job)
# APP_NAME: The name of the application, default is the registry image
# VERSION: The tag of the image, default is the CI_COMMIT_TAG if available, otherwise "merge" if CI_PIPELINE_SOURCE is merge_request_event, "latest" if CI_COMMIT_BRANCH is main, "dev" otherwise
# BUILD_ARGS: The arguments to pass to the build, default is empty
# BUILD_DIR: The directory to build the image in, default is the directory of the Dockerfile
# PLATFORMS: The platforms to build the image for, default is linux/amd64
# DOCKERFILE_PATH: The path to the Dockerfile, default is Dockerfile

#!/bin/bash
set -e

# Parse BUILD_ARGS into proper format
BUILD_ARGS_FORMATTED=""
if [ -n "$BUILD_ARGS" ]; then
  IFS=',' read -ra ARG_ARRAY <<< "$BUILD_ARGS"
  for arg in "${ARG_ARRAY[@]}"; do
    BUILD_ARGS_FORMATTED="$BUILD_ARGS_FORMATTED --build-arg $arg"
  done
fi

echo $BUILD_ARGS_FORMATTED

# Verify dockerfile exists
DOCKERFILE_PATH=${DOCKERFILE_PATH:-Dockerfile}
if [ ! -f "$DOCKERFILE_PATH" ]; then
  echo "Dockerfile not found at $DOCKERFILE_PATH"
  exit 1
fi
DOCKERFILE_DIR=$(dirname "$DOCKERFILE_PATH")
DOCKERFILE_NAME=$(basename "$DOCKERFILE_PATH")

# Get BUILD_DIR from variables and cd into it if available or use DOCKERFILE_DIR
if [ -n "$BUILD_DIR" ]; then
  cd "$BUILD_DIR"
  # Calculate relative path from BUILD_DIR to DOCKERFILE_PATH
  DOCKERFILE_NAME="${DOCKERFILE_PATH#$BUILD_DIR/}"
else
  cd "$DOCKERFILE_DIR"
fi

# Build the image
echo "Building image: ${IMAGE_TAG}"
docker buildx build --platform ${PLATFORMS:-linux/amd64} --push \
  -t "${IMAGE_TAG}" \
  $BUILD_ARGS_FORMATTED \
  -f "$DOCKERFILE_NAME" .