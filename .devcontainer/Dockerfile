# See here for image contents: https://github.com/devcontainers/images/tree/main/src/python

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3.12-bullseye, 3.11-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye
ARG VARIANT="3.12-bullseye"
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

# [Choice] Node.js version: none, lts/*, 18, 16, 14
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then \
    su vscode -c "umask 0002 && source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; \
    fi

# Install pip requirements
COPY .devcontainer/requirements.txt /tmp/pip-tmp/
RUN pip install --disable-pip-version-check --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Set PYTHONPATH for custom module paths
ENV PYTHONPATH="${PYTHONPATH}:/workspaces/neqsimpython"

# Install additional OS packages
RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
        python3-pip \
        curl \
        git \
        build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python utilities globally
RUN pip install --no-cache-dir \
    black \
    flake8 \
    pylint \
    autopep8 \
    yapf \
    bandit \
    mypy \
    pycodestyle \
    pydocstyle

# Set default user to vscode
USER vscode
