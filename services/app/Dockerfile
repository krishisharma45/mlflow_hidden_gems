# syntax=docker/dockerfile:1.2
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

WORKDIR /workspace

# Allows python to stream logs rather than buffer them for output.
ENV PYTHONUNBUFFERED=1

# The official Debian/Ubuntu Docker Image automatically removes the cache by default!
# Removing the docker-clean file manages that issue.
RUN rm -rf /etc/apt/apt.conf.d/docker-clean

RUN --mount=type=cache,mode=0777,target=/var/cache/apt apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
COPY services/app/requirements.txt  .
RUN --mount=type=cache,mode=0777,target=/root/.cache pip install --upgrade pip \
    && pip install -r requirements.txt

# Switch to non-root user
RUN useradd -m appuser && chown -R appuser /workspace
USER appuser

# Copy base files
COPY . .