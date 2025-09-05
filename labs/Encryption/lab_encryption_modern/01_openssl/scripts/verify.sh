#!/usr/bin/env bash
set -e
file="${1:?file}"; sig="${2:?signature}"; pub="${3:?public key}"
openssl dgst -sha256 -verify "$pub" -signature "$sig" "$file"
