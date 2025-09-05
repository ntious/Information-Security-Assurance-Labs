#!/usr/bin/env bash
set -e
in="${1:?encrypted file}"; out="${2:?recovered file}"
openssl enc -d -aes-256-cbc -pbkdf2 -in "$in" -out "$out"
