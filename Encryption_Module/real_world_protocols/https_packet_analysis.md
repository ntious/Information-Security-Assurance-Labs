# HTTPS Packet Analysis

## Objective
Use Wireshark to observe the difference between HTTP and HTTPS traffic.

## Steps
1. Open Wireshark and capture on your main interface.
2. In your browser, visit:
   - http://example.com
   - https://example.com
3. Stop the capture and filter by `http` and `tls`.

## What to Observe
- HTTP shows URLs and content in plaintext.
- HTTPS hides content via encryption using TLS.
