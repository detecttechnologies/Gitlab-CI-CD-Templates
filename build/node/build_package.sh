#!/bin/bash

echo "Building npm package for project: ${CI_PROJECT_NAME} with tag: ${VERSION}"
apt-get update && apt-get install -y jq
# Main build logic
if [ "$CI_PROJECT_NAME" != "tpulse-msa-fe-root-app" ]; then
  echo "Building standard application..."
  npm ci
  npm run build
  echo "Creating a distributable tarball of the dist directory"
  tar -czf "${CI_PROJECT_NAME}-${VERSION}.tar.gz" -C dist .
else
  # For root_repo, skip npm steps and create tarball without .git files
  echo "Building root application..."
  apt-get update && apt-get install -y rsync
  echo "Creating a tarball for root_repo without .git files"
  mkdir temp_dir
  rsync -av --exclude='.git' --exclude='temp_dir' --exclude='.gitlab-ci.yml' --exclude='.vscode' ./ temp_dir/
  tar -czf "${CI_PROJECT_NAME}-${VERSION}.tar.gz" -C temp_dir .
  rm -rf temp_dir
fi

echo "Uploading the tarball to GitLab's Package Registry"

# 3) Handle the commit tag package:
# 3a) Find any existing package with the same commit tag/version
EXISTING_PACKAGE_ID=$(
  curl --silent \
    --header "JOB-TOKEN: $CI_JOB_TOKEN" \
    "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages?package_type=generic&package_name=${CI_PROJECT_NAME}" \
    | jq -r ".[] | select(.version == \"${VERSION}\").id"
);
echo "Existing package ID for ${VERSION}: $EXISTING_PACKAGE_ID";
if [ -n "$EXISTING_PACKAGE_ID" ]; then
  echo "Deleting old package files for package ID $EXISTING_PACKAGE_ID for ${VERSION}...";
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
echo "Uploading package with version tag: ${VERSION}"
curl --header "JOB-TOKEN: $CI_JOB_TOKEN" \
     --upload-file "${CI_PROJECT_NAME}-${VERSION}.tar.gz" \
     "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/generic/${CI_PROJECT_NAME}/${VERSION}/${CI_PROJECT_NAME}-${VERSION}.tar.gz"