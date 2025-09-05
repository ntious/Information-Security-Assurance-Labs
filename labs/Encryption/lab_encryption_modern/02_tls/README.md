# Lab 02 — TLS/SSL in Practice

**Part A: Inspect a public TLS endpoint**
```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null
```
*Record:* TLS version, cipher suite, certificate subject, issuer, and validity dates.

**Part B: Run a tiny TLS echo server (self-signed)**
```bash
bash make_self_signed.sh
bash run_tls_server.sh
# In another terminal:
openssl s_client -connect localhost:4443 -servername localhost </dev/null
```

**Deliverables**
- One paragraph explaining how certificates enable authentication.
- Paste TLS version/cipher from Part A and a screenshot/snippet showing a successful TLS connection to localhost.
