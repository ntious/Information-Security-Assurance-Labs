#!/usr/bin/env python3
"""
Classical Ciphers Toolkit (All-in-One)
=====================================

Includes:
1. Caesar (Encrypt / Decrypt / Brute Force / Auto Decrypt)
2. Atbash (Encrypt / Decrypt, symmetric)
3. Affine (Encrypt / Decrypt, keys a & b; a must be coprime with 26)
4. Vigenere (Encrypt / Decrypt, keyword)
5. Rail Fence (Encrypt / Decrypt, transposition)
6. Columnar Transposition (Encrypt / Decrypt, keyword; pads with 'X')
7. Playfair (Encrypt / Decrypt, 5x5 grid with I/J merge; pads with 'X')
8. Hill (2x2) (Encrypt / Decrypt, matrix mod 26; pads with 'X')
9. Autokey (Encrypt / Decrypt, keyword + plaintext extension)
10. Beaufort (Encrypt/Decrypt identical, keyword)
11. Hybrid Caesar→Atbash (Encrypt / Decrypt)

Notes for students:
- Substitution ciphers here (Caesar/Atbash/Affine/Vigenere/Autokey/Beaufort/Hybrid) preserve spaces & punctuation.
- Polygraphic/transposition (Playfair/Hill/Columnar/Rail Fence) typically strip spaces or pad with 'X'.
"""

from collections import Counter
import re
import numpy as np

# -------------------------
# Shared helpers
# -------------------------
def mod_inverse(a, m=26):
    """Modular inverse via Extended Euclidean Algorithm."""
    a %= m
    if a == 0:
        raise ValueError(f"No modular inverse for a={a} under mod {m}")
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError(f"No modular inverse for a={a} under mod {m}")
    return t % m

def _require_key(key):
    if not key or not any(ch.isalpha() for ch in key):
        raise ValueError("Keyword must contain at least one alphabetic character.")

def get_step():
    while True:
        try:
            step = int(input("Enter step (1-25): "))
            if 1 <= step <= 25:
                return step
            print("Step must be 1-25.")
        except ValueError:
            print("Invalid number.")

# -------------------------
# Caesar Cipher
# -------------------------
def caesar_cipher(text, step, mode="encrypt"):
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    out = []
    if mode == "decrypt":
        step = -step
    for ch in text:
        if ch in U:
            out.append(U[(U.index(ch) + step) % 26])
        elif ch in L:
            out.append(L[(L.index(ch) + step) % 26])
        else:
            out.append(ch)
    return ''.join(out)

def brute_force_caesar(cipher_text):
    return [(step, caesar_cipher(cipher_text, step, mode="decrypt"))
            for step in range(1, 26)]

_EN_FREQ = {
    'a':8.12,'b':1.49,'c':2.71,'d':4.32,'e':12.02,'f':2.30,'g':2.03,'h':5.92,
    'i':7.31,'j':0.10,'k':0.69,'l':3.98,'m':2.61,'n':6.95,'o':7.68,'p':1.82,
    'q':0.11,'r':6.02,'s':6.28,'t':9.10,'u':2.88,'v':1.11,'w':2.09,'x':0.17,
    'y':2.11,'z':0.07
}
def _chi2_score(text):
    t = ''.join(ch.lower() for ch in text if ch.isalpha())
    n = len(t)
    if n == 0: return float('inf')
    cnt = Counter(t)
    chi = 0.0
    for c, f in _EN_FREQ.items():
        expected = f * n / 100.0
        observed = cnt.get(c, 0)
        if expected > 0:
            chi += (observed - expected) ** 2 / expected
    return chi

def auto_decrypt_caesar(cipher_text):
    candidates = []
    for step in range(1, 26):
        guess = caesar_cipher(cipher_text, step, mode="decrypt")
        score = -_chi2_score(guess)  # lower chi2 = better
        candidates.append((score, step, guess))
    candidates.sort(reverse=True)
    return candidates[0][1], candidates[0][2]

def caesar_menu():
    while True:
        print("\n--- Caesar Cipher ---")
        print("E - Encrypt | D - Decrypt | B - Brute Force | A - Auto Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt, step = input("Enter text: "), get_step()
            print("Encrypted:", caesar_cipher(txt, step, "encrypt"))
        elif choice == "D":
            txt, step = input("Enter text: "), get_step()
            print("Decrypted:", caesar_cipher(txt, step, "decrypt"))
        elif choice == "B":
            txt = input("Enter text: ")
            for s, guess in brute_force_caesar(txt):
                print(f"[{s}] {guess}")
        elif choice == "A":
            txt = input("Enter text: ")
            step, plain = auto_decrypt_caesar(txt)
            print(f"Best Step={step}, Decrypted={plain}")
        elif choice == "X": break

# -------------------------
# Atbash Cipher
# -------------------------
def atbash_cipher(text):
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    trans = {}
    for i in range(26):
        trans[U[i]] = U[25 - i]
        trans[L[i]] = L[25 - i]
    return ''.join(trans.get(ch, ch) for ch in text)

def atbash_menu():
    while True:
        print("\n--- Atbash Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice in ("E","D"):
            txt = input("Enter text: ")
            print("Result:", atbash_cipher(txt))
        elif choice == "X": break

# -------------------------
# Affine Cipher
# -------------------------
def affine_encrypt(text, a, b):
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    out = []
    for ch in text:
        if ch in U:
            out.append(U[(a * U.index(ch) + b) % 26])
        elif ch in L:
            out.append(L[(a * L.index(ch) + b) % 26])
        else:
            out.append(ch)
    return ''.join(out)

def affine_decrypt(text, a, b):
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    out = []
    inv_a = mod_inverse(a, 26)
    for ch in text:
        if ch in U:
            out.append(U[(inv_a * (U.index(ch) - b)) % 26])
        elif ch in L:
            out.append(L[(inv_a * (L.index(ch) - b)) % 26])
        else:
            out.append(ch)
    return ''.join(out)

def get_affine_keys():
    while True:
        try:
            a = int(input("Enter 'a' (must be coprime with 26): "))
            b = int(input("Enter 'b': "))
            mod_inverse(a, 26)  # validate invertibility
            return a, b
        except Exception as e:
            print("Invalid keys:", e)

def affine_menu():
    while True:
        print("\n--- Affine Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter text: "); a, b = get_affine_keys()
            print("Encrypted:", affine_encrypt(txt, a, b))
        elif choice == "D":
            txt = input("Enter text: "); a, b = get_affine_keys()
            print("Decrypted:", affine_decrypt(txt, a, b))
        elif choice == "X": break

# -------------------------
# Vigenere Cipher
# -------------------------
def vigenere_encrypt(text, key):
    _require_key(key)
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    out, key_nums, ki = [], [U.index(k.upper()) for k in key if k.isalpha()], 0
    if not key_nums:
        raise ValueError("Keyword must include letters A-Z.")
    for ch in text:
        if ch in U:
            shift = key_nums[ki % len(key_nums)]
            out.append(U[(U.index(ch) + shift) % 26]); ki += 1
        elif ch in L:
            shift = key_nums[ki % len(key_nums)]
            out.append(L[(L.index(ch) + shift) % 26]); ki += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_decrypt(text, key):
    _require_key(key)
    U, L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'
    out, key_nums, ki = [], [U.index(k.upper()) for k in key if k.isalpha()], 0
    if not key_nums:
        raise ValueError("Keyword must include letters A-Z.")
    for ch in text:
        if ch in U:
            shift = key_nums[ki % len(key_nums)]
            out.append(U[(U.index(ch) - shift) % 26]); ki += 1
        elif ch in L:
            shift = key_nums[ki % len(key_nums)]
            out.append(L[(L.index(ch) - shift) % 26]); ki += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_menu():
    while True:
        print("\n--- Vigenere Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        try:
            if choice == "E":
                txt, key = input("Enter text: "), input("Enter keyword: ")
                print("Encrypted:", vigenere_encrypt(txt, key))
            elif choice == "D":
                txt, key = input("Enter text: "), input("Enter keyword: ")
                print("Decrypted:", vigenere_decrypt(txt, key))
            elif choice == "X": break
        except Exception as e:
            print("Error:", e)

# -------------------------
# Rail Fence (Transposition)
# -------------------------
def rail_fence_encrypt(text, rails):
    if rails < 2 or not text:
        return text
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in text:
        fence[rail].append(ch)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(cipher, rails):
    if rails < 2 or not cipher:
        return cipher
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    idxs = [pattern[i % len(pattern)] for i in range(len(cipher))]
    counts = [idxs.count(r) for r in range(rails)]
    rails_str, pos = [], 0
    for count in counts:
        rails_str.append(list(cipher[pos:pos+count]))
        pos += count
    out, rail_pos = [], [0]*rails
    for r in idxs:
        out.append(rails_str[r][rail_pos[r]])
        rail_pos[r] += 1
    return ''.join(out)

def rail_fence_menu():
    while True:
        print("\n--- Rail Fence Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter text: ")
            rails = int(input("Enter number of rails: "))
            print("Encrypted:", rail_fence_encrypt(txt, rails))
        elif choice == "D":
            txt = input("Enter text: ")
            rails = int(input("Enter number of rails: "))
            print("Decrypted:", rail_fence_decrypt(txt, rails))
        elif choice == "X": break

# -------------------------
# Columnar Transposition
# -------------------------
def _keyword_order(keyword):
    pairs = [(ch, i) for i, ch in enumerate(keyword)]
    pairs.sort(key=lambda x: (x[0], x[1]))  # stable: letter then original index
    return [idx for _, idx in pairs]

def columnar_encrypt(text, keyword):
    text = text.replace(" ", "")
    cols = len(keyword)
    rows = (len(text) + cols - 1) // cols
    padded = text.ljust(rows * cols, 'X')
    matrix = [padded[i:i+cols] for i in range(0, len(padded), cols)]
    order = _keyword_order(keyword)
    cipher = ""
    for col in order:
        for row in matrix:
            cipher += row[col]
    return cipher

def columnar_decrypt(cipher, keyword):
    cols = len(keyword)
    rows = (len(cipher) + cols - 1) // cols
    order = _keyword_order(keyword)
    col_len = rows
    col_texts, pos = {}, 0
    for col in order:
        col_texts[col] = list(cipher[pos:pos+col_len])
        pos += col_len
    plain = ""
    for r in range(rows):
        for c in range(cols):
            if col_texts[c]:
                plain += col_texts[c].pop(0)
    return plain.rstrip("X")

def columnar_menu():
    while True:
        print("\n--- Columnar Transposition Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter text: ")
            key = input("Enter keyword: ")
            print("Encrypted:", columnar_encrypt(txt, key))
        elif choice == "D":
            txt = input("Enter cipher text: ")
            key = input("Enter keyword: ")
            print("Decrypted:", columnar_decrypt(txt, key))
        elif choice == "X": break

# -------------------------
# Playfair Cipher
# -------------------------
def _letters_only_upper(s):
    return re.sub(r'[^A-Z]', '', s.upper()).replace("J","I")

def generate_playfair_matrix(key):
    key = _letters_only_upper(key)
    seen, matrix = "", []
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen += ch
            matrix.append(ch)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def format_playfair_text(text):
    text = _letters_only_upper(text)
    result, i = "", 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += "X"
    return result

def find_position(matrix, ch):
    for r, row in enumerate(matrix):
        if ch in row:
            return r, row.index(ch)
    return None

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = format_playfair_text(text)
    out = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ra, ca = find_position(matrix, a)
        rb, cb = find_position(matrix, b)
        if ra == rb:  # same row
            out += matrix[ra][(ca+1)%5] + matrix[rb][(cb+1)%5]
        elif ca == cb:  # same column
            out += matrix[(ra+1)%5][ca] + matrix[(rb+1)%5][cb]
        else:  # rectangle
            out += matrix[ra][cb] + matrix[rb][ca]
    return out

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    out = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ra, ca = find_position(matrix, a)
        rb, cb = find_position(matrix, b)
        if ra == rb:  # same row
            out += matrix[ra][(ca-1)%5] + matrix[rb][(cb-1)%5]
        elif ca == cb:  # same column
            out += matrix[(ra-1)%5][ca] + matrix[(rb-1)%5][cb]
        else:  # rectangle
            out += matrix[ra][cb] + matrix[rb][ca]
    return out

def playfair_menu():
    while True:
        print("\n--- Playfair Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter text: ")
            key = input("Enter keyword: ")
            print("Encrypted:", playfair_encrypt(txt, key))
        elif choice == "D":
            txt = input("Enter cipher text: ")
            key = input("Enter keyword: ")
            print("Decrypted:", playfair_decrypt(txt, key))
        elif choice == "X": break

# -------------------------
# Hill Cipher (2×2)
# -------------------------
def char_to_num(ch): return ord(ch.upper()) - ord('A')
def num_to_char(n):  return chr(n % 26 + ord('A'))

def mod_inverse_matrix(matrix, mod=26):
    """Inverse of 2x2 matrix modulo 'mod' (no float det)."""
    a, b = int(matrix[0,0]), int(matrix[0,1])
    c, d = int(matrix[1,0]), int(matrix[1,1])
    det = (a*d - b*c) % mod
    det_inv = mod_inverse(det, mod)  # raises if not invertible
    inv = [[ d, -b],
           [-c,  a]]
    for i in range(2):
        for j in range(2):
            inv[i][j] = (det_inv * inv[i][j]) % mod
    return np.array(inv, dtype=int)

def hill_encrypt(text, key_matrix):
    text = text.replace(" ", "").upper()
    if len(text) % 2 != 0:
        text += "X"
    nums = [char_to_num(c) for c in text]
    out = ""
    for i in range(0, len(nums), 2):
        vec = np.array(nums[i:i+2])
        res = key_matrix.dot(vec) % 26
        out += ''.join(num_to_char(n) for n in res)
    return out

def hill_decrypt(cipher, key_matrix):
    inv_key = mod_inverse_matrix(key_matrix, 26)
    nums = [char_to_num(c) for c in cipher]
    out = ""
    for i in range(0, len(nums), 2):
        vec = np.array(nums[i:i+2])
        res = inv_key.dot(vec) % 26
        out += ''.join(num_to_char(int(n)) for n in res)
    return out

def hill_menu():
    while True:
        print("\n--- Hill Cipher (2x2) ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter text: ")
            print("Enter 2x2 key matrix (numbers 0-25):")
            a = int(input("a11: ")); b = int(input("a12: "))
            c = int(input("a21: ")); d = int(input("a22: "))
            key = np.array([[a, b], [c, d]], dtype=int)
            try:
                enc = hill_encrypt(txt, key)
                print("Encrypted:", enc)
            except Exception as e:
                print("Error:", e)
        elif choice == "D":
            txt = input("Enter cipher text: ")
            print("Enter 2x2 key matrix (numbers 0-25):")
            a = int(input("a11: ")); b = int(input("a12: "))
            c = int(input("a21: ")); d = int(input("a22: "))
            key = np.array([[a, b], [c, d]], dtype=int)
            try:
                dec = hill_decrypt(txt, key)
                print("Decrypted:", dec)
            except Exception as e:
                print("Error:", e)
        elif choice == "X": break

# -------------------------
# Autokey Cipher
# -------------------------
def autokey_encrypt(text, key):
    _require_key(key)
    U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    key_stream = re.sub(r'[^A-Za-z]', '', key).upper() + text
    out, ki = "", 0
    for ch in text:
        shift = U.index(key_stream[ki])
        out += U[(U.index(ch) + shift) % 26]
        ki += 1
    return out

def autokey_decrypt(cipher, key):
    _require_key(key)
    U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher = re.sub(r'[^A-Za-z]', '', cipher).upper()
    out, ki = "", 0
    key_stream = re.sub(r'[^A-Za-z]', '', key).upper()
    for ch in cipher:
        shift = U.index(key_stream[ki])
        plain = (U.index(ch) - shift) % 26
        plain_ch = U[plain]
        out += plain_ch
        key_stream += plain_ch
        ki += 1
    return out

def autokey_menu():
    while True:
        print("\n--- Autokey Cipher ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        try:
            if choice == "E":
                txt = input("Enter plaintext: ")
                key = input("Enter keyword: ")
                print("Encrypted:", autokey_encrypt(txt, key))
            elif choice == "D":
                txt = input("Enter ciphertext: ")
                key = input("Enter keyword: ")
                print("Decrypted:", autokey_decrypt(txt, key))
            elif choice == "X": break
        except Exception as e:
            print("Error:", e)

# -------------------------
# Beaufort Cipher
# -------------------------
def beaufort_cipher(text, key):
    _require_key(key)
    U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    key_nums = [U.index(k.upper()) for k in key if k.isalpha()]
    if not key_nums:
        raise ValueError("Keyword must include letters A-Z.")
    out, ki = "", 0
    for ch in text:
        shift = key_nums[ki % len(key_nums)]
        out += U[(shift - U.index(ch)) % 26]
        ki += 1
    return out

def beaufort_menu():
    while True:
        print("\n--- Beaufort Cipher ---")
        print("E - Encrypt/Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        try:
            if choice == "E":
                txt = input("Enter text: ")
                key = input("Enter keyword: ")
                print("Result:", beaufort_cipher(txt, key))
            elif choice == "X": break
        except Exception as e:
            print("Error:", e)

# -------------------------
# Hybrid Caesar -> Atbash
# -------------------------
def hybrid_encrypt(plain_text, step):
    return atbash_cipher(caesar_cipher(plain_text, step, "encrypt"))

def hybrid_decrypt(cipher_text, step):
    return caesar_cipher(atbash_cipher(cipher_text), step, "decrypt")

def hybrid_menu():
    while True:
        print("\n--- Hybrid (Caesar -> Atbash) ---")
        print("E - Encrypt | D - Decrypt | X - Back")
        choice = input("Choice: ").strip().upper()
        if choice == "E":
            txt = input("Enter plaintext: ")
            step = get_step()
            print("Encrypted:", hybrid_encrypt(txt, step))
        elif choice == "D":
            txt = input("Enter ciphertext: ")
            step = get_step()
            print("Decrypted:", hybrid_decrypt(txt, step))
        elif choice == "X":
            break

# -------------------------
# Main Menu
# -------------------------
def main():
    while True:
        print("\n=== Classical Ciphers Toolkit ===")
        print("1 - Caesar | 2 - Atbash | 3 - Affine | 4 - Vigenere")
        print("5 - Rail Fence | 6 - Columnar | 7 - Playfair | 8 - Hill")
        print("9 - Autokey | 10 - Beaufort | 11 - Hybrid (Caesar→Atbash) | Q - Quit")
        choice = input("Choose: ").strip().upper()
        if choice == "1": caesar_menu()
        elif choice == "2": atbash_menu()
        elif choice == "3": affine_menu()
        elif choice == "4": vigenere_menu()
        elif choice == "5": rail_fence_menu()
        elif choice == "6": columnar_menu()
        elif choice == "7": playfair_menu()
        elif choice == "8": hill_menu()
        elif choice == "9": autokey_menu()
        elif choice == "10": beaufort_menu()
        elif choice == "11": hybrid_menu()
        elif choice == "Q":
            print("Goodbye!"); break

if __name__ == "__main__":
    main()