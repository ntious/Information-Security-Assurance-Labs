# GPG Email Simulation

## Objective
Understand how GPG (GNU Privacy Guard) encrypts and signs email.

## Steps
1. Install GPG: `sudo apt install gnupg`
2. Generate key: `gpg --gen-key`
3. Export public key: `gpg --armor --export your_email@example.com`
4. Encrypt a file: `gpg -e -r your_email@example.com plaintext.txt`
5. Decrypt it: `gpg -d encrypted_file.gpg`

This simulates email encryption using public-key cryptography.
