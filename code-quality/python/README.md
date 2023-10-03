# Python Code Quality

Can be pulled directly from [dockerhub](https://hub.docker.com/repository/docker/detecttechnologies/python-code-quality)

```bash
docker pull detecttechnologies/python-code-quality:latest
```

To build it from the `Dockerfile`, run `docker build -t python-code-quality .`



## Building and pushing a multi-arch image

* Setup docker
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```

* Setup docker buildx
    docker buildx create --use
    ```

* If you're on an x86 platform, enable building for Arm architectures by running `docker run --rm --privileged docker/binfmt:a7996909642ee92942dcd6cff44b9b95f08dad64` (Adopted from [this docker blog post](https://www.docker.com/blog/getting-started-with-docker-for-arm-on-linux/))
    * You can update the commit hash above to the latest commit of docker/binfmt, as mentioned in the blogpost

* Login to the docker registry where you would like to push the image (generate and apply a token for the same)
    ```
    docker login
    ```

* Create a multi-arch build and push it
    ```bash
    docker buildx build --no-cache --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6 --tag detecttechnologies/python-code-quality --push .
    ```

* Test the image you just pushed with
    ```
    docker rmi detecttechnologies/python-code-quality   # Delete any older local version
    docker run --rm -v $(pwd):/workspace detecttechnologies/python-code-quality sh -c "cd /workspace && ruff ."
    ```

* Re-tag the multi-arch build with your current timestamp (**UPDATE THE 3rd LAST WORD**) and push it
    ```bash
    docker buildx build --no-cache --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6 --tag detecttechnologies/python-code-quality:<YY>-<MM> --push .
    ```

