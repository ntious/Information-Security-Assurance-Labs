import hashlib

def compute_hash(filepath, algo='sha256'):
    with open(filepath, 'rb') as f:
        file_bytes = f.read()

    if algo == 'sha256':
        hash_val = hashlib.sha256(file_bytes).hexdigest()
    elif algo == 'sha1':
        hash_val = hashlib.sha1(file_bytes).hexdigest()
    elif algo == 'md5':
        hash_val = hashlib.md5(file_bytes).hexdigest()
    else:
        raise ValueError("Unsupported hashing algorithm.")

    return hash_val

def compare_files(file1, file2, algo='sha256'):
    hash1 = compute_hash(file1, algo)
    hash2 = compute_hash(file2, algo)
    return hash1 == hash2

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python hash_compare.py <file1> <file2>")
    else:
        match = compare_files(sys.argv[1], sys.argv[2])
        print("Files match:" if match else "Files differ.")
