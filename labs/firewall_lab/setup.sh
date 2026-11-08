#!/usr/bin/env bash
set -eu

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This setup script requires an Ubuntu/Debian system with apt-get." >&2
  exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
  SUDO=
elif command -v sudo >/dev/null 2>&1; then
  SUDO=sudo
else
  echo "Run as root or install sudo before continuing." >&2
  exit 1
fi

$SUDO apt-get update
$SUDO apt-get install -y --no-install-recommends ufw curl netcat-openbsd openssl python3
