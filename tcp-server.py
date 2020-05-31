#!/usr/bin/env python3

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = ("127.0.0.1", 1338)
backlog = 1
chunk_size = 16

print("Running on %s:%s" % addr)

sock.bind(addr)
sock.listen(backlog)


def handle(conn):
    try:
        while True:
            data = conn.recv(16)
            if data:
                print(data)
                conn.sendall(b"OK\n")
            else:
                break
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
        print("Connection closed.")


while True:
    conn, addr = sock.accept()
    print("conn from:", addr)

    handle(conn)
