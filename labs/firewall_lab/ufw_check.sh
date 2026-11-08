#!/usr/bin/env bash
set -u

if ! command -v ufw >/dev/null 2>&1; then
  echo "UFW is not installed. Run bash setup.sh first." >&2
  exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
  UFW_PREFIX=()
elif command -v sudo >/dev/null 2>&1; then
  UFW_PREFIX=(sudo)
else
  echo "This check needs root privileges or sudo." >&2
  exit 1
fi

if ! status=$("${UFW_PREFIX[@]}" ufw status verbose); then
  echo "Could not read UFW status." >&2
  exit 1
fi
if ! rules=$("${UFW_PREFIX[@]}" ufw status numbered); then
  echo "Could not read numbered UFW rules." >&2
  exit 1
fi

printf '%s\n' "=== UFW STATUS (VERBOSE) ===" "$status"
failed=0

if printf '%s\n' "$status" | grep -Eqi '^Status:[[:space:]]+active'; then
  echo "PASS: UFW is active"
else
  echo "FAIL: UFW is not active"
  failed=1
fi

if printf '%s\n' "$status" | grep -Eqi 'Default: deny \(incoming\), allow \(outgoing\)'; then
  echo "PASS: default policy is deny incoming / allow outgoing"
else
  echo "FAIL: default policy is not deny incoming / allow outgoing"
  failed=1
fi

check_rule() {
  local rule="$1"
  local pattern="$2"
  if printf '%s\n' "$rules" | grep -Eiq "$pattern"; then
    echo "PASS: $rule"
  else
    echo "FAIL: missing rule $rule"
    failed=1
  fi
}

check_rule "allow TCP 8000" '^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]+8000/tcp[[:space:]]+ALLOW IN'
check_rule "allow TCP 8443" '^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]+8443/tcp[[:space:]]+ALLOW IN'
check_rule "deny TCP 21" '^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]+21/tcp[[:space:]]+DENY IN'
check_rule "deny TCP 23" '^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]+23/tcp[[:space:]]+DENY IN'

if [ "$failed" -eq 0 ]; then
  echo "Checker passed."
else
  echo "Checker failed. Review the lab instructions and rerun."
fi
exit "$failed"