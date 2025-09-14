#!/bin/bash

echo "Building npm package for project: ${CI_PROJECT_NAME} with tag: ${VERSION}"
# Main build logic
if [ "$BUILD_DIST" = "true" ]; then
  echo "BUILD_DIST is true - running npm build..."
  npm ci
  npm run build
  echo "Creating a distributable tarball of the dist directory"
  tar -czf "${CI_PROJECT_NAME}-${VERSION}.tar.gz" -C dist .
else
  echo "BUILD_DIST is false - creating tarball without npm build..."
  echo "Creating a tarball without .git files"
  mkdir temp_dir
  rsync -av --exclude='.git' --exclude='temp_dir' --exclude='.gitlab-ci.yml' --exclude='.vscode' ./ temp_dir/
  tar -czf "${CI_PROJECT_NAME}-${VERSION}.tar.gz" -C temp_dir .
  rm -rf temp_dir
fi

echo "Uploading the tarball to GitLab's Package Registry"

# Display tarball size information
TARBALL_SIZE=$(du -h "${CI_PROJECT_NAME}-${VERSION}.tar.gz" | cut -f1)
echo "Tarball size: ${TARBALL_SIZE}"


# 3) Handle the commit tag package:
# 3a) Find any existing package with the same commit tag/version
GITLAB_API_BASE="https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages"


EXISTING_PACKAGE_ID=$(
  curl --silent \
    --header "JOB-TOKEN: $CI_JOB_TOKEN" \
    "${GITLAB_API_BASE}?package_type=generic&package_name=${CI_PROJECT_NAME}" \
    | jq -r ".[] | select(.version == \"${VERSION}\").id"
);
echo "Existing package ID for ${VERSION}: $EXISTING_PACKAGE_ID";
if [ -n "$EXISTING_PACKAGE_ID" ]; then
  echo "Deleting old package files for package ID $EXISTING_PACKAGE_ID for ${VERSION}...";
  PACKAGE_FILE_IDS=$(
    curl --silent \
      --header "JOB-TOKEN: $CI_JOB_TOKEN" \
      "${GITLAB_API_BASE}/${EXISTING_PACKAGE_ID}/package_files" \
      | jq -r ".[].id"
  );
  for FILE_ID in $PACKAGE_FILE_IDS; do
    curl --request DELETE \
         --header "JOB-TOKEN: $CI_JOB_TOKEN" \
         "${GITLAB_API_BASE}/${EXISTING_PACKAGE_ID}/package_files/${FILE_ID}";
  done
fi

# 3b) Upload the new release.zip for the commit tag
echo "Uploading package with version tag: ${VERSION}"
curl --header "JOB-TOKEN: $CI_JOB_TOKEN" \
     --upload-file "${CI_PROJECT_NAME}-${VERSION}.tar.gz" \
     "${GITLAB_API_BASE}/generic/${CI_PROJECT_NAME}/${VERSION}/${CI_PROJECT_NAME}-${VERSION}.tar.gz"