# 🧩 Classical Ciphers Toolkit

This Python toolkit is an **interactive playground for classical cryptography**.  
It allows students to explore, encrypt, decrypt, and experiment with **11 major historical ciphers**.

---

## ✨ Features

The toolkit includes:

1. **Caesar Cipher**
   - Encrypt / Decrypt
   - Brute Force (try all 25 keys)
   - Auto Decrypt (statistical guess)
2. **Atbash Cipher** (symmetric)
3. **Affine Cipher** (Encrypt / Decrypt with `a` and `b` keys)
4. **Vigenère Cipher** (Encrypt / Decrypt with keyword)
5. **Rail Fence Cipher** (Transposition, Encrypt / Decrypt with rails)
6. **Columnar Transposition Cipher** (Encrypt / Decrypt with keyword)
7. **Playfair Cipher** (5×5 grid, digraph encryption, pads with `X`)
8. **Hill Cipher (2×2)** (Encrypt / Decrypt with matrix key, pads with `X`)
9. **Autokey Cipher** (Encrypt / Decrypt, key extended with plaintext)
10. **Beaufort Cipher** (Encrypt / Decrypt with keyword, same function)
11. **Hybrid Caesar → Atbash** (Encrypt with Caesar, then Atbash)

---

## 🚀 Getting Started

### Requirements
- Python **3.7+**
- `numpy` library (for Hill cipher math):
  ```bash
  pip install numpy
````

### Running

Run the toolkit directly:

```bash
python classical_ciphers_toolkit.py
```

You’ll see a main menu:

```
=== Classical Ciphers Toolkit ===
1 - Caesar | 2 - Atbash | 3 - Affine | 4 - Vigenere
5 - Rail Fence | 6 - Columnar | 7 - Playfair | 8 - Hill
9 - Autokey | 10 - Beaufort | 11 - Hybrid (Caesar→Atbash) | Q - Quit
Choose:
```

---

## 🕹️ Usage Guide

Each cipher has its own sub-menu. Typical flow:

* **Encrypt:** type text + key(s) → see ciphertext.
* **Decrypt:** type ciphertext + key(s) → recover plaintext.
* Some strip spaces and pad with `X` (Hill, Playfair, Columnar).

---

## 📚 Cipher Details

### Caesar

* Shift each letter by N (step).
* Example: `HELLO`, step=3 → `KHOOR`.

### Atbash

* Reverse alphabet substitution (A↔Z, B↔Y).
* Example: `HELLO` → `SVOOL`.

### Affine

* Formula: `E(x) = (a·x + b) mod 26`.
* Requires two keys: `a` (coprime with 26) and `b`.

### Vigenère

* Keyword-based Caesar shifts.
* Example: `HELLO`, key=`KEY` → `RIJVS`.

### Rail Fence

* Write letters in zigzag rails, read row by row.
* Example (3 rails): `HELLO WORLD` → `HOOLELWRDL`.

### Columnar

* Write in grid under keyword, read by column order.
* Example: keyword=`ZEBRA`, `HELLO WORLD` → `LWDLOOERHLX`.

### Playfair

* 5×5 grid of letters with keyword.
* Works on digraphs, pads with `X` if needed.
* Example: keyword=`MONARCHY`, text=`HELLO WORLD` → `KBMODZBXDM`.

### Hill (2×2)

* Uses 2×2 matrix multiplication mod 26.
* Example: key=\[\[3,3],\[2,5]], text=`HELLO` → `MFNCX`.

### Autokey

* Like Vigenère but key is extended with plaintext.
* Example: text=`HELLOWORLD`, key=`KEY`.

### Beaufort

* Formula: `C = (K - P) mod 26`.
* Same function used for encryption & decryption.

### Hybrid Caesar → Atbash

* Apply Caesar shift, then Atbash.
* Example: text=`HELLO`, step=3 → Caesar=`KHOOR` → Atbash=`PSLLI`.

---

## ✅ Quick Sanity Tests

Students can try these right away:

```
Caesar:    "HELLO", step=3 → Encrypted: KHOOR → back: HELLO
Atbash:    "HELLO WORLD" → Encrypted: SVOOL DLIOW → back: HELLO WORLD
Affine:    a=5, b=8, "HELLO" → Encrypted: RCLLA → back: HELLO
Vigenere:  key=KEY, "HELLO" → Encrypted: RIJVS → back: HELLO
RailFence: rails=3, "HELLO WORLD" → Encrypted: HOOLELWRDL → back: HELLO WORLD
Columnar:  key=ZEBRA, "HELLO WORLD" → Encrypted: LWDLOOERHLX → back: HELLOWORLD
Playfair:  key=MONARCHY, "HELLO WORLD" → Encrypted: KBMODZBXDM → back: HELXLOWORLDX
Hill:      key=[[3,3],[2,5]], "HELLO" → Encrypted: MFNCX → back: HELLOX
Autokey:   key=KEY, "HELLOWORLD" → Encrypted (try and decrypt back)
Beaufort:  key=KEY, "HELLO" → Encrypted: DRJIY → back: HELLO
Hybrid:    step=3, "HELLO" → Encrypted: PSLLI → back: HELLO
```

---

## 📖 Learning Notes

* **Substitution ciphers** (Caesar, Affine, Vigenère, etc.) change *letters*.
* **Transposition ciphers** (Rail Fence, Columnar) rearrange *positions*.
* **Polygraphic ciphers** (Playfair, Hill) work on *pairs/blocks* of letters.
* **Autokey & Beaufort** show how Vigenère can be extended.
* **Hybrid** combines ciphers, showing layered security.

---

## 🛠️ Extending the Toolkit

* Add new ciphers (ROT13, Bacon’s, Enigma simulation).
* Add non-interactive CLI with `argparse` to script encryption.
* Encourage students to break these ciphers with frequency analysis!

---

🎓 **Enjoy exploring classical cryptography!**

```
### By I. K. NTI for educational purpose only