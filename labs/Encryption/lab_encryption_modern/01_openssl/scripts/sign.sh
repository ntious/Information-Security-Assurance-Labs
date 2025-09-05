#!/usr/bin/env bash
set -e
file="${1:?file}"; sig="${2:?signature out}"; key="${3:?private key}"
openssl dgst -sha256 -sign "$key" -out "$sig" "$file"
