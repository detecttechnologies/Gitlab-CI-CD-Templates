#!/bin/bash
set -e

# Set IMAGE_NAME
if [ -z "$APP_NAME" ]; then
  IMAGE_NAME="${CI_REGISTRY_IMAGE}"
  echo "APP_NAME not provided, defaulting to: $IMAGE_NAME"
else
  IMAGE_NAME="${CI_REGISTRY_IMAGE}/${APP_NAME}"
fi

# Parse BUILD_ARGS into proper format
BUILD_ARGS_FORMATTED=""
if [ -n "$BUILD_ARGS" ]; then
  IFS=',' read -ra ARG_ARRAY <<< "$BUILD_ARGS"
  for arg in "${ARG_ARRAY[@]}"; do
    BUILD_ARGS_FORMATTED="$BUILD_ARGS_FORMATTED --build-arg $arg"
  done
fi

echo $BUILD_ARGS_FORMATTED

# Extract directory and filename from DOCKERFILE_PATH
DOCKERFILE_PATH=${DOCKERFILE_PATH:-Dockerfile}
DOCKERFILE_DIR=$(dirname "$DOCKERFILE_PATH")
DOCKERFILE_NAME=$(basename "$DOCKERFILE_PATH")

# Verify dockerfile exists
if [ ! -f "$DOCKERFILE_PATH" ]; then
  echo "Dockerfile not found at $DOCKERFILE_PATH"
  exit 1
fi

# Navigate to directory if not in root
if [ "$DOCKERFILE_DIR" != "." ]; then
  echo "Changing to directory: $DOCKERFILE_DIR"
  cd "$DOCKERFILE_DIR"
fi

# Build the image
echo "Building image: ${IMAGE_NAME}:${VERSION}"
docker buildx build --platform ${PLATFORMS:-linux/amd64} --push \
  -t "${IMAGE_NAME}:${VERSION}" \
  $BUILD_ARGS_FORMATTED \
  -f "$DOCKERFILE_NAME" .
