#!/usr/bin/env bash
set -e
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  openssl curl ca-certificates iputils-ping openssh-client
python -m pip install --no-cache-dir --upgrade pip
