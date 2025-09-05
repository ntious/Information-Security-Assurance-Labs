#!/usr/bin/env bash
set -e
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3 -nodes -subj "/CN=localhost"
