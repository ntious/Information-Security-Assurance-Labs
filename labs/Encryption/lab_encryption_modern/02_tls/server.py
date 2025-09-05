import ssl, socket
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('0.0.0.0', 4443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            data = conn.recv(1024)
            if data:
                conn.sendall(data)  # echo
            conn.close()
