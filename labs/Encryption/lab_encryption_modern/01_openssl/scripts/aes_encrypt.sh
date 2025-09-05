#!/usr/bin/env bash
set -e
in="${1:?input file}"; out="${2:?output file}"
openssl enc -aes-256-cbc -salt -pbkdf2 -in "$in" -out "$out"
