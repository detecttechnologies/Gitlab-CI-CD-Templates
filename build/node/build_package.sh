#!/bin/bash

echo "Building npm package for project: ${CI_PROJECT_NAME} with tag: ${CI_COMMIT_TAG}"

# Main build logic
if [ "$CI_PROJECT_NAME" != "tpulse-msa-fe-root-app" ]; then
  echo "Building standard application..."
  npm ci
  npm run build
  echo "Creating a distributable tarball of the dist directory"
  tar -czf "${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tar.gz" -C dist .
else
  # For root_repo, skip npm steps and create tarball without .git files
  echo "Building root application..."
  apt-get update && apt-get install -y rsync
  echo "Creating a tarball for root_repo without .git files"
  mkdir temp_dir
  rsync -av --exclude='.git' --exclude='temp_dir' --exclude='.gitlab-ci.yml' --exclude='.vscode' ./ temp_dir/
  tar -czf "${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tar.gz" -C temp_dir .
  rm -rf temp_dir
fi

echo "Uploading the tarball to GitLab's Package Registry"

# 3) Handle the commit tag package:
# 3a) Find any existing package with the same commit tag/version
EXISTING_PACKAGE_ID=$(
  curl --silent \
    --header "JOB-TOKEN: $CI_JOB_TOKEN" \
    "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages?package_type=generic&package_name=${CI_PROJECT_NAME}" \
    | jq -r ".[] | select(.version == \"${CI_COMMIT_TAG}\").id"
);
echo "Existing package ID for ${CI_COMMIT_TAG}: $EXISTING_PACKAGE_ID";
if [ -n "$EXISTING_PACKAGE_ID" ]; then
  echo "Deleting old package files for package ID $EXISTING_PACKAGE_ID for ${CI_COMMIT_TAG}...";
  PACKAGE_FILE_IDS=$(
    curl --silent \
      --header "JOB-TOKEN: $CI_JOB_TOKEN" \
      "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/${EXISTING_PACKAGE_ID}/package_files" \
      | jq -r ".[].id"
  );
  for FILE_ID in $PACKAGE_FILE_IDS; do
    curl --request DELETE \
         --header "JOB-TOKEN: $CI_JOB_TOKEN" \
         "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/${EXISTING_PACKAGE_ID}/package_files/${FILE_ID}";
  done
fi

# 3b) Upload the new release.zip for the commit tag
echo "Uploading package with version tag: ${CI_COMMIT_TAG}"
curl --header "JOB-TOKEN: $CI_JOB_TOKEN" \
     --upload-file "${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tar.gz" \
     "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/generic/${CI_PROJECT_NAME}/${CI_COMMIT_TAG}/${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tar.gz"

# 4) Handle the "latest" tag package:
# 4a) Find any existing package with the "latest" version
EXISTING_PACKAGE_ID_LATEST=$(
  curl --silent \
    --header "JOB-TOKEN: $CI_JOB_TOKEN" \
    "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages?package_type=generic&package_name=${CI_PROJECT_NAME}" \
    | jq -r ".[] | select(.version == \"latest\").id"
);
echo "Existing package ID for latest: $EXISTING_PACKAGE_ID_LATEST";
if [ -n "$EXISTING_PACKAGE_ID_LATEST" ]; then
  echo "Deleting old package files for package ID $EXISTING_PACKAGE_ID_LATEST for latest...";
  PACKAGE_FILE_IDS_LATEST=$(
    curl --silent \
      --header "JOB-TOKEN: $CI_JOB_TOKEN" \
      "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/${EXISTING_PACKAGE_ID_LATEST}/package_files" \
      | jq -r ".[].id"
  );
  for FILE_ID in $PACKAGE_FILE_IDS_LATEST; do
    curl --request DELETE \
         --header "JOB-TOKEN: $CI_JOB_TOKEN" \
         "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/${EXISTING_PACKAGE_ID_LATEST}/package_files/${FILE_ID}";
  done
fi

# 4b) Upload the new release.zip for the "latest" tag
echo "Uploading package with latest tag"
cp "${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tar.gz" "${CI_PROJECT_NAME}-latest.tar.gz"
curl --header "JOB-TOKEN: $CI_JOB_TOKEN" \
     --upload-file "${CI_PROJECT_NAME}-latest.tar.gz" \
     "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/generic/${CI_PROJECT_NAME}/latest/${CI_PROJECT_NAME}-latest.tar.gz"

echo "Build and upload completed successfully!"