# Python Compilation

Compiles python files for distribution in different python versions and CPU achitectures

NOTE: The files are not statically compiled, and hence any pypi dependencies will still have to be installed

## Troubleshooting

1. If you see this error in the CI pipeline FOR the `build-armv7` job:
    ```bash
    Skipping Git submodules setup
    Executing "step_script" stage of the job script 00:00
    Using docker image sha256:1df7cf6223b8bc56f843f3c80d268253c5656ad4ba5913dcbb6123572b07182f for registry.gitlab.com/detecttechnologies/platform/ci-cd-pipelines/python-ops/pycompiler:1.0-armv7 with digest registry.gitlab.com/detecttechnologies/platform/ci-cd-pipelines/python-ops/pycompiler@sha256:aa88d8444af2774fcab8e4952855d499729ed36e2cc76b447cf1bcb727259a9b ...
    exec /usr/bin/sh: exec format error
    Cleaning up project directory and file based variables 00:01
    ERROR: Job failed: exit code 1
    ```
    You will have to re-run that particular job after some time. The root cause of this issue is not yet diagnosed.
    <br>

2. If you see this error in your CI pipeline logs for the final stage:
    ```bash
    $ echo 'Running on the Detect Gitlab CI/CD runner with timestamp: xxx'
    Running on the Detect Gitlab CI/CD runner with timestamp: xxx
    $ mkdir ~/.ssh/
    $ which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )
    /usr/bin/ssh-agent
    $ ssh-keyscan -t rsa $CI_SERVER_HOST >> ~/.ssh/known_hosts
    # gitlab.com:22 SSH-2.0-GitLab-SSHD
    $ echo "${SSH_PUSH_KEY}" > ~/.ssh/id_rsa
    $ chmod 600 ~/.ssh/id_rsa
    $ git config --global user.email "PlatformTeam@detecttechnologies.com"
    $ git config --global user.name "DetectTechnologies CI"
    $ git clone "${BUILD_OUTPUT_REPO}" /root/dest
    Cloning into '/root/dest'...
    Warning: Permanently added the RSA host key for IP address 'xxx' to the list of known hosts.
    remote: 
    remote: ========================================================================
    remote: 
    remote: ERROR: The project you were looking for could not be found or you don't have permission to view it.
    remote: 
    remote: ========================================================================
    remote: 
    fatal: Could not read from remote repository.
    Please make sure you have the correct access rights
    and the repository exists.
    Cleaning up project directory and file based variables 00:00
    ERROR: Job failed: exit code 1
    ```
    It is likely because you need to enable the `SSH_PUSH_KEY` in your Destination Repository's `Deploy Keys` section
    <br>
    
3. If you see this error in your CI pipeline logs for the final stage:
    ```bash
    $ git push origin HEAD:main -f
    remote: 
    remote: ========================================================================
    remote: 
    remote: ERROR: This deploy key does not have write access to this project.
    remote: 
    remote: ========================================================================
    remote: 
    fatal: Could not read from remote repository.
    Please make sure you have the correct access rights
    and the repository exists.
    Cleaning up project directory and file based variables 00:00
    ERROR: Job failed: exit code 1
    ```
    It is likely because you need to enable write access for your Deploy Key in the Destination repositorey