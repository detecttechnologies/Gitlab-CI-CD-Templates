#!/bin/bash

#remove the temp worktree
git worktree remove temp-worktree || true

# if CI_COMMIT_BRANCH is main, get the latest tag
if [ "$CI_COMMIT_BRANCH" = "main" ]; then
    export TAG=$(git describe --abbrev=0 --tags)
else
    export TAG=$CI_COMMIT_SHA
fi

# create a temp worktree and build the dist
git worktree add temp-worktree $TAG

# create a symlink to the node_modules folder
ln -s $CI_PROJECT_DIR/node_modules temp-worktree/node_modules

# build the dist 
cd temp-worktree
npm run build
cd ..