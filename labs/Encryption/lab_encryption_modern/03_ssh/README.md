# Lab 03 — SSH Keys & Secure Remote

**Steps**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/student_key -C "student@example.com"
cat ~/.ssh/student_key.pub   # add to GitHub → Settings → SSH and GPG keys
ssh-keyscan github.com >> ~/.ssh/known_hosts
ssh -i ~/.ssh/student_key -T git@github.com   # identity test, no shell
```

**Explain**
- How host keys + known_hosts protect against MITM.
- Why key-based auth > passwords.

**Deliverable**
- One paragraph: SSH vs TLS (use cases, trust model).
