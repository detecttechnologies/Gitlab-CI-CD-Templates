# Inspired from https://github.com/cytopia/docker-black

FROM alpine:latest as builder

RUN set -eux \
    && apk add --no-cache \
    bc \
    gcc \
    musl-dev \
    py3-pip \
    python3 \
    python3-dev

# Install the needed libs first system-wide, create a backup. Then install for the user, and cache the binaries alone for reuse later
# (Because we can't use the /usr/bin folder during system-wide install, it will have additional files from gcc, etc)
RUN set -eux \
    && pip3 install --no-cache-dir --no-compile black ruff \
    && black --version \
    # Since python versions being used in alpine will keep changing, the below command caches the site-packages in a temp dir
    && cp -r $(python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))") /root/python-site-pkgs \
    && pip3 uninstall -y black ruff \
    && pip3 install --no-cache-dir --no-compile --user black ruff


FROM alpine:latest as production

LABEL maintainer="Detect Technologies Pvt. Ltd."

COPY --from=builder /root/python-site-pkgs /root/python-site-pkgs
COPY --from=builder /root/.local/bin/* /usr/bin/

RUN set -eux \
    && apk add --no-cache python3 \
    && mv /root/python-site-pkgs/* $(python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))") \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf \
    && find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -rf

