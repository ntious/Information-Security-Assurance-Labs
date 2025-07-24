def read_text(path):
    with open(path, 'r') as f:
        return f.read()

def write_text(path, content):
    with open(path, 'w') as f:
        f.write(content)
