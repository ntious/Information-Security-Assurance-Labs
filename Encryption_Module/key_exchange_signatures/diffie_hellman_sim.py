# Simulated Diffie-Hellman Key Exchange (simplified, not secure)

def mod_exp(base, exponent, mod):
    return pow(base, exponent, mod)

def simulate_diffie_hellman():
    P = 23  # prime
    G = 5   # primitive root

    a = 6  # Alice's private key
    b = 15 # Bob's private key

    A = mod_exp(G, a, P)  # Alice sends A
    B = mod_exp(G, b, P)  # Bob sends B

    shared_key_alice = mod_exp(B, a, P)
    shared_key_bob = mod_exp(A, b, P)

    print(f"Alice's key: {shared_key_alice}")
    print(f"Bob's key:   {shared_key_bob}")
    assert shared_key_alice == shared_key_bob

if __name__ == "__main__":
    simulate_diffie_hellman()
