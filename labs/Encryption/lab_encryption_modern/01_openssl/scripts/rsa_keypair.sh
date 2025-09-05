#!/usr/bin/env bash
#Students generate private.pem and public.pem using rsa_keypair.sh.
set -e
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out private.pem
openssl rsa -pubout -in private.pem -out public.pem
