#!/usr/bin/env bash
set -e
echo "=== UFW STATUS (VERBOSE) ==="
sudo ufw status verbose

fail=0
check_rule () {
  local pattern="$1"
  if sudo ufw status numbered | grep -E "$pattern" >/dev/null; then
    echo "✓ Rule present: $pattern"
  else
    echo "✗ Missing rule: $pattern"; fail=1
  fi
}

# Expected baseline
sudo ufw status | grep -qi "Status: active" && echo "✓ UFW is active" || { echo "✗ UFW not active"; fail=1; }
sudo ufw status verbose | grep -qi "Default: deny (incoming), allow (outgoing)" \
  && echo "✓ Default policy correct" || { echo "✗ Default policy not correct"; fail=1; }

# Required port rules (adjust if you change lab spec)
check_rule "22/tcp.*ALLOW"
check_rule "80/tcp.*ALLOW"
check_rule "443/tcp.*ALLOW"
check_rule "21/tcp.*DENY"
check_rule "23/tcp.*DENY"

echo
if [ $fail -eq 0 ]; then
  echo "✅ Checker passed."
  exit 0
else
  echo "❌ Checker failed. Fix missing items above and re-run."
  exit 1
fi
