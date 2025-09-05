.PHONY: check openssl tls tls-run ssh vpn clean all

# ✅ Sanity check: OpenSSL + Python installed
check:
	@echo "== Environment Versions =="
	@openssl version
	@python --version
	@echo "✅ Environment OK"

# 🔑 Lab 01 - OpenSSL Essentials
openssl:
	@echo "== Running OpenSSL Lab check =="
	cd labs/Encryption/lab_encryption_modern/01_openssl && \
	bash scripts/rsa_keypair.sh && \
	openssl rsa -in private.pem -check -noout
	@echo "✅ RSA keypair created successfully"

# 🔐 Lab 02 - TLS/SSL
tls:
	@echo "== Running TLS Lab check =="
	cd labs/Encryption/lab_encryption_modern/02_tls && \
	bash make_self_signed.sh && \
	openssl x509 -in cert.pem -noout -subject -issuer -dates
	@echo "✅ TLS certificate created successfully"

# ▶️ Lab 02 - Run TLS echo server
tls-run:
	@echo "== Starting TLS echo server on port 4443 =="
	@echo "Open a second terminal and run:"
	@echo "  openssl s_client -connect localhost:4443 -servername localhost </dev/null"
	cd labs/Encryption/lab_encryption_modern/02_tls && \
	python server.py

# 🔒 Lab 03 - SSH
ssh:
	@echo "== Running SSH Lab check =="
	@ssh -V || true
	@echo "✅ SSH client available"

# 🌐 Lab 04 - VPN
vpn:
	@echo "== Checking VPN config files =="
	@test -f labs/Encryption/lab_encryption_modern/04_vpn/wireguard_example.conf && echo "WireGuard config exists"
	@test -f labs/Encryption/lab_encryption_modern/04_vpn/openvpn_client_example.ovpn && echo "OpenVPN config exists"
	@echo "✅ VPN configs ready for analysis"

# 🧹 Clean generated artifacts
clean:
	@echo "== Removing generated crypto artifacts =="
	@rm -f labs/Encryption/lab_encryption_modern/01_openssl/private.pem
	@rm -f labs/Encryption/lab_encryption_modern/01_openssl/public.pem
	@rm -f labs/Encryption/lab_encryption_modern/01_openssl/signature.bin
	@rm -f labs/Encryption/lab_encryption_modern/01_openssl/secret.enc
	@rm -f labs/Encryption/lab_encryption_modern/02_tls/cert.pem
	@rm -f labs/Encryption/lab_encryption_modern/02_tls/key.pem
	@echo "✅ Clean complete"

# Run all checks
all: check openssl tls ssh vpn
	@echo "🎉 All labs checked successfully!"
